The file `grade.py` is a zero-dependency CSV editor **with tab completion** aimed at helping TAs quickly record grades. (Windows users may need Cygwin or WSL2. If you are having trouble, let me know.) You download a CSV of student grades from Blackboard, run the script, give it the path to the CSV file when prompted, choose if you want to assign grades by **name** or by **ID number**, and choose which assignment to grade. It then prompts you for names or ID numbers (which can be entered only partially then tab completed) and the corresponding grades. It is most useful for grading paper assignments, which are often received out of alphabetical order.

```
$ cat test.csv
First,Last,UIN,First Quiz,Second Quiz
John,Boyle,38291,,9
Bob,Palermo,91823,0,
Lucy,Burke,11928,,
John,Santora,83921,3,9

$ python3 grade.py 
Path to grades csv: <TAB><TAB>
grade.py  README.md test.csv 
Path to grades csv: te<TAB>
test.csv

Assign grades by
1) Name
2) UIN
(type the number without quotes, then press Return): 1

Which column corresponds to FIRST NAME?
1) First
2) First Quiz
(type the number without quotes, then press Return): 1

Which column corresponds to LAST NAME?
1) Last
(type the number without quotes, then press Return): 1

Type the name of the assessment exactly as it appears on Blackboard (case sensitive).
> <TAB><TAB>
First       First Quiz  Last        Second Quiz UIN        
> Se<TAB>
> Second Quiz

Begin grading.
Type QUIT at the prompt to stop grading and write file.

Student: Lu<TAB>
Lucy Burke
Grade: 98

Student: John<TAB><TAB> 
John Boyle   John Santora
Student: John S<TAB>
John Santora
Grade: 92

Student: Bob<TAB>
Bob Palermo
Grade: 98

Student: John Boyle
Grade: 84

Student: QUIT

Successfully wrote grades to updated_grades.csv.

$ cat updated_grades.csv 
First,Last,UIN,First Quiz,Second Quiz
John,Boyle,38291,,84
Bob,Palermo,91823,0,98
Lucy,Burke,11928,,98
John,Santora,83921,3,92
```
