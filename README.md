# Anti-Cheating Implementation within a Virtualized Learning Environment

This document highlights the Objectives and Key Results for the Anti-Cheating within a Virtualized Learning Environment. The module will focus on monitoring the student activity and analysis of the submission. The prior focuses on working with the hypervisor to log student logins and file activity. While the latter focuses mainly on submission comparison and run-time characteristics like cycles used and resources accessed. Based on the threshold set by the TA or instructor previously each submission is checked and tagged for deceptive activity. 

## Student Workflow  
The student interacts with the platform using a Web API and SSH. The assignment is released and visible to the student on the Web GUI. The student can be in the following states: 
* Waiting for assignment to be released 
* Working on the assignment 
* Has submitted the assignment and is pending grading 
* Has received the grade for the assignment

The project implementation focuses on the second and third  stages. 

1. When student is working on their assignment
    
    While the student is actively working on thier assignment, the system records the following tasks: 
    - The VM monitoring system for the student directory, is saves the current contents at a fixed time interval. 
    - Process monitoring system which intercepts and records student activity.

2. When student has submitted their work for grading 
    - The submit script installed within their root directory packs up the folder and logs to the evaluation system. 
    - The evaluation system takes user code, grader script from the TA and database values to match and score results. 
    - The evaluation system uses a static plagerism to check the distance between submission files. 
    - Further, the system will be running a byte-code analysis to map out similarity in execution of the file. 

## Task Lists 
### General Scripts 
- [x] Setup Scripts for making the MYSQL database
- [x] Control Program 
- [ ] Analysis of collected metrics
### Plagerism Check
- [x] Static Checker in Rust 
- [x] Integration with the backend system
### Dynamic Check 
~~ - [ ] Implementation using gdb ~~
- [x] Time taken to run the student code 
- [x] Grading with the TA script
- [ ] Integration with the backend system
### Student Parameters 
~~ - [ ] Installing version control system ~~
- [ ] Recomiling the OS with custom code 
- [ ] Integrating with SSH/VS code system
- [ ] Integrating with backend system 

### Future Additions 
~~ - [ ] Integration with MOSS ~~

## Team Members
Priyansh Singh, Jayant Mishra, Kshitij, Satyam Modi, Arka Mandal and Abhijith

 
<!-- 
Here is a very. broad overview of what I’m thinking here:
1.     (Static) Doing a similarity/distance comparison of the student submission
2.     (Dynamic) Runtime eval with time, access and other metrics 
3.     Combining the two into a confidence score to determine if the student is cheating
We can use some rudimentary training algorithm and sample randomly from the given submissions
 
@ the time of student actively interacting with the system,
Ø  Hypervisor to log more details at the time when the user is coding. 
Ø  Simple Heuristic to match  
Ø  Logging of the number of times the file has been modified 
Ø  Time Log, delta from the deadline 
 
Ø  Usage pattern of the VM
Ø  Using a threshold to flag and not reject
 
Ø  How many cycles and memory usage for auto-grading 
 
Ø  Some form of pattern matching on VM memory utilisation 
 
OKRs should be measurable 
 
Diagram and implementation 
 
 
Write a script At the time of user ask for an autograder and profiles a file. Use it  to run score and save the results
 -->
