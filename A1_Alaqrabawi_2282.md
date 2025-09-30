Student ID: 20322282
Name: Yusuf Alaqrabawi 
Group Number: 1

Project Implementation Status

| Function | Implementation      | Missing Items                                                                                                                                   |
|----------|---------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| R1: Add book           | Partial             | ISBN field does not check for non-digit characters                                                                                       |
| R2: Book catalog display | Complete           | None                                                                                                                                    |
| R3: Book borrowing      | Complete           | None                                                                                                                                    |
| R4: Book returning      | Partial            | Does not verify book was borrowed by patron. Does not update available copies. Does not record return date. Does not calculate/display fees owed |
| R5: late fee                     | No implementation   | Not implemented entirely                                                                                                                |
| R6: book search                     | Partial            | Does not support ISBN, title, or author search. Does not return any results                                                              |
| R7: patron status                     | No implementation   | Functionality not implemented entirely, no menu option to view patron status                                                             |

Unit Test 

for each requirment function there are 4 unit testing, 2 that should succeed and 2 that should fail. 
invalid Patron/book/ISBN/NAMES were used in the unit testing to test things that should return false.