""" Hash Table ADT

Defines a Hash Table using Linear Probing for conflict resolution.
"""
from __future__ import annotations


__author__ = 'Brendon Taylor. Modified by Graeme Gange, Alexey Ignatiev, and Jackson Goerner'
__docformat__ = 'reStructuredText'
__modified__ = '21/05/2020'
__since__ = '14/05/2020'


from referential_array import ArrayR
from typing import TypeVar, Generic
T = TypeVar('T')


class LinearProbeTable(Generic[T]):
    """
        Linear Probe Table.

        attributes:
            count: number of elements in the hash table
            table: used to represent our internal array
            tablesize: current size of the hash table
    """

    def __init__(self, expected_size: int, tablesize_override: int = -1) -> None:
        """
            Initialiser.
            Best and worse case complexity: O(N), N is the size of the hashtable
        """

        self.count = 0
        if tablesize_override == -1:
            self.table = ArrayR(expected_size * 2)  # this needs to be prime, will use vincent's code
            self.tablesize = expected_size * 2
        else:
            self.table = ArrayR(tablesize_override)
            self.tablesize = tablesize_override
        self.rehash_count = 0
        self.conflict_count = 0
        self.conflict_bool = False
        self.probe_list = []        # this is used to determine the longest probe chain

    def hash(self, key: str) -> int:
        """
            Hash a key for insertion into the hashtable.
            Best and worst case: O(N), N is the length of the string
        """

        value = 0 
        hashbase = 31
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.tablesize
            a = a * hashbase % (self.tablesize - 1)

        return value


    def statistics(self) -> tuple:
        """
            Hash a key for insertion into the hashtable.
            Best and worst case: O(N), N is the length of the length of the list
        """ 
        #conflict_count = how many times conflicts occur throughout the exceution of the code 
        #probe_total = total distance probed
        #probe_max = longest probe chain 
        #rehash_count = number of times rehashing was done 

        #conflict count: Set bool to TRUE if "position = (position + 1) % len(self.table)" is runs. If TRUE return += 1 (every time _linear_probe is called)
        #probe_total = count how many times "position = (position + 1) % len(self.table)" is runs.
        #probe_max = could keep appending the no hashes to a list, then max(list)
        #rehash_count = add counter in rehash function, ez.

        # self.conflict_bool will be used 
        if self.conflict_bool:
            self.conflict_count += 1
        
        # if len(self.probe_list) == 0:
        #     probe_max = 0        
        probe_max = max(self.probe_list)
        probe_total = sum(self.probe_list)

        return(self.conflict_count, probe_total, probe_max, self.rehash_count)

    def __len__(self) -> int:
        """
            Returns number of elements in the hash table
            :complexity: O(1)
        """
        return self.count

    def _linear_probe(self, key: str, is_insert: bool) -> int:
        """
            Find the correct position for this key in the hash table using linear probing
            :complexity best: O(K) first position is empty
                            where K is the size of the key
            :complexity worst: O(K + N) when we've searched the entire table
                            where N is the tablesize
            :raises KeyError: When a position can't be found
        """

        if self.conflict_bool:
            self.conflict_count += 1

        self.conflict_bool = False   # hasnt been a conflict yet
        self.probe_temp = 0

        position = self.hash(key)  # get the position using hash

        if is_insert and self.is_full():
            raise KeyError(key)

        for _ in range(len(self.table)):  # start traversing
            if self.table[position] is None:  # found empty slot
                if is_insert:
                    self.probe_list.append(self.probe_temp)
                    return position
                else:
                    raise KeyError(key)  # so the key is not in
            elif self.table[position][0] == key:  # found key
                self.probe_list.append(self.probe_temp)     # chucking it in a list to determien the max later 
                return position
            else:  # there is something but not the key, try next
                position = (position + 1) % len(self.table)

                self.conflict_bool = True
                self.probe_temp += 1
        raise KeyError(key)

    def keys(self) -> list[str]:
        """
            Returns all keys in the hash table.
            best and worst case: O(N), N = length of the hashtable
        """
        res = []
        for x in range(len(self.table)):
            if self.table[x] is not None:
                res.append(self.table[x][0])
        return res

    def values(self) -> list[T]:
        """
            Returns all values in the hash table.
            best and worst case: O(N), N = length of the hashtable
        """
        res = []
        for x in range(len(self.table)):
            if self.table[x] is not None:
                res.append(self.table[x][1])
        return res

    def __contains__(self, key: str) -> bool:
        """
            Checks to see if the given key is in the Hash Table
            :see: #self.__getitem__(self, key: str)
            best case: complexity best: O(K) first position is empty
                            where K is the size of the key
            worst case: complexity worst: O(K + N) when we've searched the entire table
                            where N is the tablesize
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: str) -> T:
        """
            Get the item at a certain key
            :see: #self._linear_probe(key: str, is_insert: bool)
            :raises KeyError: when the item doesn't exist
            best case: complexity best: O(K) first position is empty
                            where K is the size of the key
            worst case: complexity worst: O(K + N) when we've searched the entire table
                            where N is the tablesize
        """
        position = self._linear_probe(key, False)
        return self.table[position][1]

    def __setitem__(self, key: str, data: T) -> None:
        """
            Set an (key, data) pair in our hash table
            :see: #self._linear_probe(key: str, is_insert: bool)
            :see: #self.__contains__(key: str)
            best case: complexity best: O(K) first position is empty
                            where K is the size of the key
            worst case: complexity worst: O(K + N + R) when we've searched the entire table
                            where N is the tablesize, R is the complexity for rehashing
        """

        if self.count > self.tablesize // 2:
            self._rehash()



        position = self._linear_probe(key, True)

        if self.table[position] is None:
            self.count += 1

        self.table[position] = (key, data)



    def is_empty(self):
        """
            Returns whether the hash table is empty
            :complexity: O(1)
        """
        return self.count == 0

    def is_full(self):
        """
            Returns whether the hash table is full
            :complexity: O(1)
        """
        return self.count == len(self.table)

    def insert(self, key: str, data: T) -> None:
        """
            Utility method to call our setitem method
            :see: #__setitem__(self, key: str, data: T)
            best case = O(K)
            worst case = O(K + N + R), same as set item
        """
        self[key] = data

    def _rehash(self) -> None:          
        """
            Need to resize table and reinsert all values
            best case: O(length of new_table + K), forming a new table and then inserting elements in 
            worst case: O(K + N + length of table)
        """
        self.rehash_count += 1
        keys_list = self.keys()
        value_list = self.values()
        self.tablesize =(2 * self.tablesize)
        self.table = ArrayR(len(self.table) * 2)
        self.count = 0
        for i in range(len(keys_list)):
            self[keys_list[i]] = value_list[i]    # this should rehash 
          

    def __delitem__(self, key: str):
        """Reinsert every after deletion.
        best case: O(K)
        worst case: O(K + N + C), C is the cluster 
        """
        position = self._linear_probe(key, False)
        self.table[position] = None
        self.count -= 1
        position = (position + 1) % self.tablesize
        while self.table[position] is not None:
            key2, value = self.table[position]
            self.table[position] = None
            newpos = self._linear_probe(key2, True)
            self.table[newpos] = (key2, value)
            position = (position + 1) % self.tablesize

    def __str__(self) -> str:
        """
            Returns all they key/value pairs in our hash table (no particular
            order).
            :complexity: O(N) where N is the table size
        """
        result = ""
        for item in self.table:
            if item is not None:
                (key, value) = item
                result += "(" + str(key) + "," + str(value) + ")\n"
        return result


class NewTable(LinearProbeTable):
    def __init__(self, expected_size: int, hashbase: int, tablesize_override: int = -1) -> None:
        super().__init__(expected_size, tablesize_override)
        self.hashbase = hashbase

    def hash(self, key: str) -> int:
       
        """
            Hash a key for insertion into the hashtable.
            Best and worst case: O(N), N is the length of the string
        """

        value = 0 
        # hashbase = 9929
        self.hashbase
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.tablesize
            a = a * self.hashbase % (self.tablesize - 1)

        return value

