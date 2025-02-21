# **Report for assignment 3**

## **Project**

Name: Python Utility Bot

URL: https://github.com/python-discord/bot

This project is a Discord bot specifically for use with the Python Discord server. It provides numerous utilities and other tools to help keep the server running like a well-oiled machine.

## **Onboarding experience**

### **Build Process Review**

*(a) Installation of Additional Tools* 

The Python version needs to be moved down to 3.12.\* for this to work. For this we used a virtual environment that used python version 3.12.\*. 

The only required tool mentioned in the documentation for building the project was Poetry. We had no issues downloading it. After installing Poetry, we went into the virtual environment and ran the command `poetry install` and successfully installed all dependencies. 

*(b) Documentation Quality* 

The tools were well-documented, making the setup process straightforward. 

*(c) Automatic Installation of Components*

No additional components were installed automatically by the build script.

*(d) Build Process and Errors* 

The build process did not conclude automatically. To proceed, we had to manually add a .env file with the following lines: 

`BOT_TOKEN=00`  
`GUILD_ID=00`  
This step was necessary to successfully build and run tests. 

(e) Performance of Examples and Tests 

All examples and tests ran smoothly on our systems without any errors. One of them was skipped.

### **Future plans**

We plan to continue working on this project rather than switching to another one.

## **Complexity**

1. *What are your results for five complex functions?*  
   * *Did all methods (tools vs. manual count) get the same result?*  
   * *Are the results clear?*  
2. *Are the functions just complex, or also long?*  
3. *What is the purpose of the functions?*  
4. *Are exceptions taken into account in the given measurements?*  
5. *Is the documentation clear w.r.t. all the possible outcomes?*

Manual calculation was done according to the formula from [this source](https://radon.readthedocs.io/en/latest/intro.html#cyclomatic-complexity)

### **Function 1:**

In search.py: search\_criteria\_converter()

1. Results from counting CC manually and using lizard  
* Felicia: Counted CC \= 18, counted 17 decision points \+ 1  
* Elias: Counted CC \= 18, counted 17 decision points \+ 1  
* Lizard counted CC \= 18  
2. As both what we manually calculated and what lizard calculated, the CC of this function is 18 which is moderately complex. The function is also long, with an LOC og approximately 53\.  
3. Purpose of the function, can it be related to the high CC?: The search\_criteria\_converter function parses and validates input data representing setting overrides. It takes dictionaries for filter lists, loaded filters, settings, filter settings, a filter type, and an input string. It returns a tuple containing processed settings, filter settings, and the filter type.  
   The function checks if the input is empty and returns default values if so. It splits the input data by a delimiter, parses the settings, and raises an error if the format is incorrect. It processes a \--template setting if present, then validates and converts the remaining settings based on predefined types. If a template is specified, it merges its settings with the provided ones. Finally, it returns the validated settings, filter settings, and filter type.  
   Because of this the purpose of this function can be related to the high CC. There are a lot of validations being made.  
4. Python uses try/except statements which all added \+1 to the CC in our manual calculations. Because we got the same result as lizard, lizard seems count those aswell.  
5. No, there is no dedicated documentation for it but there are a few code comments for the if statements.

### **Function 2:**

In filtering.py: send\_weekly\_auto\_infraction\_report()

1. Results from counting CC manually and using lizard  
   * Felicia counted: Counted CC \= 18, 17 decision points \+ 1  
   * Riccardo counted: Counted CC \= 18, 17 decision points \+ 1  
   * Lizard counted CC \= 18  
2. Both lizard and the manual calculations yielded the same cyclomatic complexity with CC \= 18\. With 49 LOC the function is moderate size but contains multiple branching conditions.  
   Most of the complexity arises from the numerous scenarios that the function tries to handle.  
3. The function extracts infractions added in the last 7 days, categorizes them, and sends a formatted report. If the report exceeds Discord's message length limit, it attempts to upload it to a paste service and, if that fails, attaches it as a file.  
4. The function contains two explicit exception handlers (discord.HTTPException and PasteUploadError), contributing to its CC.  
5. The function contains some well-written comments that explain the reporting process, however, some edges case are not documented.

### **Function 3:**

In filter.py: description\_and\_settings\_converter()

1. Result from manual counting of the CC and the lizard tool:  
* Elias: Counted CC \= 18, 17 decision points \+ 1  
* Riccardo: Counted CC \= 18, 17 decision points \+ 1  
* Lizard counted CC \= 18  
2. Both lizard and the manual calculations yielded the same cyclomatic complexity with CC \= 18\. With 55 LOC the function is also relatively large.  
3. description\_and\_settings\_converter parses the input string of setting overrides and descriptions. It separates out a description and extracts filter list/filter settings. It validates them, applies any template overrides, and returns a tuple with the description and two dictionaries of settings. The high CC is directly related to the multiple input cases required by the purpose of the function.  
4. Multiple try/except statements are used which increases the CC as stated earlier  
5. No, similarly to function 1, comments here and there describing some if statements, but no documentation for outcomes of the function

### **Function 4:**

In internal.py: \_format()

1. Result from manual counting of the CC and the lizard tool:  
   * Felicia: Counted CC \= 17, 16 decision points \+ 1  
   * Dmitry: Counted CC \= 17, 16 decision points \+ 1  
   * Lizard counted CC \= 17  
2. The function is most likely more complex than it should be, combining multiple purposes and actions together, also making it long in our case. This can simply be mitigated by splitting different logic parts into different smaller functions, without compromising any functionality, also making it simpler to properly test different parts of the function.  
3. The function tries to format the input into the form of an embed. To do that, it goes through several steps, which can all be separated.  
4. As with the previous functions, the added \+1 to the CC count comes from the way Python handles functions, by adding a try-catch clause.  
5. No, it only describes what the input and output are, but not what possible outcomes can be produced by the function. Some comments describe the output of that part of the function though.

### **Function 5:**

In filter.py: update\_embed()

1. Result from manual counting of the CC and the lizard tool:  
* Felicia: counted CC \= 20, 19 decision points \+ 1  
* Riccardo: counted CC \= 20, 19 decision points \+ 1  
* Lizard counted CC \= 20  
2. Both lizard and the manual calculations yielded a cyclomatic complexity scores with CC \= 20\. With 75 LOC the function is also relatively large, likely larger than it needs to be.  
3. The purpose of update\_embed is to refresh the visual embed for the Discord UI element based on inputs, such as updating content, description, and settings overrides. The high cyclomatic complexity comes from the need to handle these multiple cases and decision points.  
4. There is one try/except statement in the function, adding 1 to the CC  
5. The docstring specifies some of the outcomes but could be more detailed

## **Coverage**

### **Tools**

*How well was the tool documented? Was it possible/easy/difficult to integrate it with your build environment?*

We used Coverage.py to check the coverage of the code. In our virtual environment we installed it by using the command `pip install coverage` 

Then, running command `coverage run --branch -m pytest tests` it ran all the tests and then running command `coverage html` we got html files that we could run in our browser to look at the coverage for each function.

### **Your own coverage tool**

Link to our [coverage tool](https://github.com/SoffanDD2480/assignment-3-CODE-COVERAGE/blob/Issue/3-implement-branch-coverage-tool/tests/branch_coverage_tool.py)

The tool we implemented is fairly simple. For each function that we wanted to measured, we created a python dictionary that tracks the id:s of the visited branches in a specific function specified by the given function id; this dictionary works like a map. 

First you needed to import the `branch_coverage_tool` module to the file where the function is, and above the function name, add `@instrument_function`

In each function we measured we identified every branching point where we added a `track_branch(func_id, branch_id)`function call. This added each visited branch to the dictionary. In the branch\_coverage tool we needed to specify how many branches in total a function has

In the functions, at each branching point we just made sure to add the branch\_id to the dictionary. In the end, after all tests have been run the results are written to a txt file in the coverage\_report/ directory.

*What kinds of constructs does your tool support, and how accurate is its output?*

The tool supports if, else, for, while, try/except. It can support any branch point.

### **Evaluation**

1. *How detailed is your coverage measurement?*  
2. *What are the limitations of your own tool?*  
3. *Are the results of your tool consistent with existing coverage tools?*

#### Coverage measurement details

1. **Function-Level Tracking:**  
   1. It tracks branches per function, but it does not track the number of times each branch is taken, only whether it has been visited at least once.  
2. **Basic Branch Coverage:**  
   1. It records branch IDs in a dictionary, meaning it can tell if a branch has been visited but does not capture paths through multiple branches.  
3. **Report Generation:**  
   1. It saves a report with a timestamp, showing which branches have been executed and the overall percentage of branch coverage for the functions that are measured.

The tool generates a file and 

#### Limitations of the tool

**Static Total Branch Count per Function:**

The `total_branches` value is hardcoded for each function ID and is missing dynamic detection of how many branches exist in other functions.

**Manual Branch Tracking Required:**

To measure branch coverage in a function, you must explicitly call `track_branch(func_id, branch_id)`at each branching point, which makes instrumentation tedious. Also it can make the measurement wrong since you have to rely on that you have counted the amount of branches correctly.

**No Path Coverage Measurement:**

It does not track execution paths (i.e., sequences of branches taken in combination).

This means that while it tracks whether a branch has been visited, it does not show whether all logical paths through a function have been tested.

#### Results 

The result from our tool might differ from coverage.py because of the limitations. OUr tool is very sensitive to human error in counting the branches and there are some cases where it won't be able to count a branch, for instance a if statement or for-loop inside a dictionary, in these cases, we had to refactor the code to refactor the code a bit to be able to put our tracker inside the if-statements and for loop that the tool can’t reach. This can be a bit difficult.

## **Coverage improvement**

To be able to run some of our tests cases, we needed to run the following command `pip install pytest_asyncio` in our virtual environment

### **Felicia Murkes: Function 1**

Test for function search\_criteria\_converter() (Path: tests/bot/test\_search.py):  
[https://github.com/SoffanDD2480/assignment-3-CODE-COVERAGE/blob/main/tests/bot/test\_search.py](https://github.com/SoffanDD2480/assignment-3-CODE-COVERAGE/blob/main/tests/bot/test_search.py)

Requirements That were tested or untested:

- The function was not tested at all

Identified requirements to test:

- Valid input (Positive flow) so that we can reach the final return statement  
- Invalid Filter, raises exception  
- Invalid setting, raises exception  
- No input data, return in the beginning of the function

The tests added:

test\_search\_criteria\_converter\_valid(mock\_parse\_value)  
test\_search\_criteria\_converter\_invalid\_filter(mock\_parse\_value)  
test\_invalid\_setting()  
test\_search\_criteria\_no\_input\_data(mock\_parse\_value)

With coverage.py  
Branch coverage before: 0%  
Branch coverage after: 53%

Our tool  
Branch coverage before: 0%  
Branch coverage after: 51.7%

### **Riccardo Cocco: Function 2**

Test for function send\_weekly\_auto\_infraction\_report()   
(Path: tests/bot/exts/filtering/test\_filtering.py):  
[https://github.com/SoffanDD2480/assignment-3-CODE-COVERAGE/blob/main/tests/bot/exts/filtering/test\_filtering.py](https://github.com/SoffanDD2480/assignment-3-CODE-COVERAGE/blob/main/tests/bot/exts/filtering/test_filtering.py)

Requirements That were tested or untested:

- The function was not tested

Identified requirements to test:

- Behaviour when no channel is provided  
- Exit condition when the channel is not a mod channel  
- Return message when no infractions is provided  
- When filters exist, the function should correctly format the report  
- The function should only include filters added in the last 7 days, excluding the older ones.

The test added:

- test\_send\_report\_no\_channel  
- test\_send\_report\_non\_mod\_channel  
- test\_send\_report\_no\_filters  
- test\_send\_report\_with\_filters

with coverage.py  
Branch coverage before: 0%  
Branch coverage after: 71%

Our tool  
Branch coverage before: 0%  
Branch coverage after: 63.2% (12/19 branches)

### **Elias Fröde: Function 3**

Function descriptions\_and\_settings\_coverter()   
(Path: tests/bot/test\_descriptions\_and\_settings\_converter.py):

[https://github.com/SoffanDD2480/assignment-3-CODE-COVERAGE/blob/main/tests/bot/test\_descriptions\_and\_settings\_converter.py](https://github.com/SoffanDD2480/assignment-3-CODE-COVERAGE/blob/main/tests/bot/test_descriptions_and_settings_converter.py)

Requirements That were tested or untested:  
The function was not tested at all prior.  
Identified requirements to test:

- Return of Empty input  
- Description only input, lacks setting pattern  
- Return for a valid filter list setting  
- Return for a valid filter extra field setting

The tests added:

- test\_empty\_input()  
- test\_only\_description()  
- test\_filter\_list\_setting\_override()  
- test\_filter\_extra\_field\_override()

With coverage.py  
Branch coverage before: 0%  
Branch coverage after: 66%

Our tool  
Branch coverage before: 0%  
Branch coverage after: 53.8% (14/26 branches)

### **Dmitry Chirin: Function 4**

It was not possible to create the tests without an instance of the \`Internal\` class. After making that one, with a \`MockBot\` for the \`Bot\` class, and for specific tests used an instance of \`Embed\` class. All of that was added to the setUp function to make each test independent, and act in the intended way.

All branches are not covered, as well as all the combinations of the branches. Some branches are not covered by either tool, being list comprehension. In this case, our tool can’t reach the “second” branch of the for loop, so our tool doesn’t count it as a branch, although coverage.py does that.

Tests for function \_format() (Path: tests/bot/exts/utils/test\_internal.py):  
[https://github.com/SoffanDD2480/assignment-3-CODE-COVERAGE/blob/main/tests/bot/exts/utils/test\_internal.py](https://github.com/SoffanDD2480/assignment-3-CODE-COVERAGE/blob/main/tests/bot/exts/utils/test_internal.py)

Requirements That were tested or untested:

- The function was not tested at all

Identified requirements to test:

- Valid input (Positive flow) so that we can reach the final return statement  
- Invalid Filter, raises exception  
- Invalid setting, raises exception  
- No input data, return in the beginning of the function

The tests added:

test\_format\_no\_input()  
test\_format\_embed()  
test\_get\_input\_dialog\_empty\_list()  
test\_get\_input\_dialog\_return()  
test\_get\_prettified\_dict()  
test\_get\_prettified\_compact()

With coverage.py:

* Branch coverage before: 0%  
* Branch coverage after: 85%

Our tool:

* Branch coverage before: 0%  
* Branch coverage after: 76%

### 

### **Albin Wallenius Woxnerud: Function 5**

Function update\_embed (bot/exts/filtering/\_ui/filter.py) tests are located in the following file:  
tests/bot/exts/filtering/test\_ui\_filter.py

https://github.com/SoffanDD2480/assignment-3-CODE-COVERAGE/blob/main/tests/bot/exts/filtering/test\_ui\_filter.py

Requirements that were tested or untested:  
The function was not tested at all prior.  
Identified requirements to test:

* Ensure valid content updates the embed correctly.  
* Handle invalid content gracefully by sending an error message and preventing updates.  
* Allow descriptions to be removed when \_REMOVE is specified.  
* Ensure long descriptions are truncated to MAX\_EMBED\_DESCRIPTION.  
* Verify that settings with a slash (/) update filter\_settings\_overrides.  
* Verify that settings without a slash update settings\_overrides.  
* Ensure settings reset when set to their default values.  
* Ensure settings overrides are removed when set to \_REMOVE.  
* Differentiate behavior between discord.Message and discord.Interaction when editing.  
* Handle HTTP exceptions when attempting to edit messages, ensuring the view does not stop unexpectedly.

The tests added:

* test\_valid\_content\_with\_description(): Verifies that the embed updates when given valid content and a description.  
* test\_invalid\_content(): Ensures an error message is sent and the embed remains unchanged when invalid content is provided.  
* test\_remove\_description(): Confirms that setting the description to \_REMOVE clears it properly.  
* test\_embed\_description\_truncated(): Ensures long descriptions are truncated to fit within MAX\_EMBED\_DESCRIPTION.  
* test\_setting\_with\_slash\_and\_override(): Verifies that settings with slashes update filter\_settings\_overrides.  
* test\_setting\_without\_slash\_and\_override(): Ensures settings without slashes update settings\_overrides.  
* test\_setting\_equal\_default\_removes\_override(): Checks that settings set to their default values remove any overrides.  
* test\_setting\_remove(): Ensures that setting a value to \_REMOVE properly removes it from overrides.  
* test\_message\_vs\_interaction\_edit(): Tests handling of discord.Message and discord.Interaction separately.  
* test\_edit\_message\_http\_exception(): Ensures that an HTTP exception while editing does not stop the view unexpectedly.

With coverage  
Branch coverage before: 0%  
Branch coverage after: 92%

Our tool  
Branch coverage before: 0%  
Branch coverage after: 86.7% (26/30 branches)

## **Refactoring**

### **Function 1: search\_criteria\_converter()**

There are 5 main parts that can be made into helper functions in the search\_criteria\_converter function to make it have less CC. 

The original function performs multiple independent tasks, such as:

* Parsing input data.  
* Determining filter types.  
* Validating settings.  
* Handling filter-specific settings.  
* Applying template settings.

Each of these responsibilities can be put into a separate helper function, reducing the complexity of `search_criteria_converter`. The drawback of this is since we’ve divided the functions into 5 parts, the lack of tests might cause the refactoring to create new bugs.

###### *After carrying out the refactor:*

Link to refactored function:  
[https://github.com/SoffanDD2480/assignment-3-CODE-COVERAGE/blob/refactor-funcs/bot/exts/filtering/\_ui/search.py](https://github.com/SoffanDD2480/assignment-3-CODE-COVERAGE/blob/refactor-funcs/bot/exts/filtering/_ui/search.py)

These are the helper functions that would be made:

* parse\_input\_data(input\_data: str) \-\> dict\[str, str\]  
  * Splits the input string and constructs a dictionary of settings.  
  * Handles format validation.  
  * CC \= 4  
* resolve\_filter\_type(filter\_name: str, filter\_type: type\[Filter\] | None, loaded\_filters: dict) \-\> type\[Filter\]  
  * Determines the appropriate filter type based on the given filter name.  
  * CC \= 2  
* validate\_and\_parse\_settings(settings: dict, loaded\_settings: dict) \-\> dict  
  * Validates general settings and converts them to their correct types.  
  * CC \= 5  
* validate\_and\_parse\_filter\_settings(settings: dict, filter\_type: type\[Filter\], loaded\_filter\_settings: dict) \-\> dict  
  * Validates filter-specific settings.  
  * CC \= 5  
* \`apply\_template\_settings(template: str, filter\_lists: dict, settings: dict, filter\_settings: dict, filter\_type: type\[Filter\]) \-\> tuple\[dict, dict, type\[Filter\]\]\`  
  * Loads template settings and merges them with user-provided settings.  
  * CC \= 2  
* search\_criteria\_converter which is the original function now has a CC of 4

### **Function 2:**

The original function send\_weekly\_auto\_infraction\_report performed multiple independent tasks, including:

- Determining the appropriate channel for sending the report.  
- Extracting and categorizing auto-infractions added in the last 7 days.  
- Formatting the extracted data for reporting.  
- Sending the report to the specified channel while handling potential errors.

###### *After carrying out the refactor:*

Link to refactored function:  
[https://github.com/SoffanDD2480/assignment-3-CODE-COVERAGE/blob/refactor-funcs/bot/exts/filtering/filtering.py](https://github.com/SoffanDD2480/assignment-3-CODE-COVERAGE/blob/refactor-funcs/bot/exts/filtering/filtering.py)

To reduce CC and improve readability, the function was refactored by introducing helper functions:

* resolve\_channel(channel: discord.TextChannel | discord.Thread | None) \-\> discord.TextChannel | discord.Thread | None  
  * Determines the appropriate channel for sending the report.  
  * CC \= 3 , 2 decision points \+ 1  
* collect\_recent\_auto\_infractions(seven\_days\_ago) \-\> dict  
  * Extracts all auto-infraction filters added in the past 7 days.  
  * CC \= 10, 9 decision points \+ 1  
* format\_report(found\_filters: dict, seven\_days\_ago) \-\> str  
  * Formats the report by grouping auto-infractions by category.  
  * CC \= 3, 2 decision points \+ 1  
* send\_report(channel: discord.TextChannel | discord.Thread, report: str)  
  * Sends the report to the specified channel, handling potential content length errors.  
  * CC \= 4, 3 decision points \+ 1

Implementing this brings down the CC of the original function to 2 which is much lower than the original 18\.

**Function 3:**  
The original function description\_and\_settings\_converter performs multiple independent tasks, including:  
\- Extracting description part of parsed input.  
\- Creating settings dict and checking for "--template" entry  
\- Handling cases for filter/filter-list settings.

All of which increases the CC, especially processing the filter/filter-list settings. A possible refactoring is then to create helper functions for each of these tasks in order to decrease the CC of the original function. 

Link to refactored function: [https://github.com/SoffanDD2480/assignment-3-CODE-COVERAGE/blob/refactor-funcs/bot/exts/filtering/\_ui/filter.py](https://github.com/SoffanDD2480/assignment-3-CODE-COVERAGE/blob/refactor-funcs/bot/exts/filtering/_ui/filter.py) 

###### *After carrying out the refactor:*

These are the helper functions implemented:

* extract\_description(\_parsed: list\[str\]) \-\> tuple\[str, list\[str\]\]  
  * Checks parsed input for description.  
  * CC \= 2   
* create\_settings\_dict(parts: list\[str\]) \-\> dict\[str, str\]  
  * Constructs the settings dictionary in the same way as the original function.  
  * CC \= 3  
* extract\_template(settings: dict\[str, str\]) \-\> tuple\[None | str, dict\[str, str\]\]  
  * Extract the template setting if provided, and remove it from the settings dictionary.  
  * CC \= 2  
* process\_settings(settings: dict\[str, str\], filter\_list: FilterList, list\_type: ListType, filter\_type: type\[Filter\], loaded\_settings: dict, loaded\_filter\_settings: dict) \-\> tuple\[dict\[str, Any\], dict\[str, Any\]\]:  
  * Process setting overrides and separates them into list and filter-specific settings.  
  * CC \= 6 Note: In order to further bring down the CC of process\_settings (originally at 10\) the following 2 functions were also implemented:  
* process\_list\_setting(key: str, settings: dict\[str, str\], filter\_list: FilterList, list\_type: ListType, loaded\_settings: dict) \-\> Any:  
  * Processes the list settings similarly to the original function.  
  * CC \= 3  
* process\_filter\_setting(key: str, settings: dict\[str, str\], filter\_type: type\[Filter\], loaded\_filter\_settings: dict) \-\> tuple\[str, Any\]  
  * Processing the filter-specific settings Similarly to the original function.  
  * CC \= 5

Implementing this brings down the CC of the original function to 5 which is much lower than the original 18\.

### **Function 4:**

The function \_format could be split into lots of different parts, and the parts into smaller parts themselves to reduce CC, for example by following the Clean Code principles, keeping the CC very low. In our case, however, it should suffice to split the function into 3 similar sized parts (CC-wise), splitting the logical parts into their own function. This way, we have two new functions in addition to the original one:

###### *After carrying out the refactor:*

* def \_format(self, inp: str, out: Any) \-\> tuple\[str, discord.Embed | None\]:   
  * **Original function**  
  * Format the eval output into a string & attempt to format it into an Embed  
  * CC: 7, 6 decision points \+ 1  
* def get\_input\_dialog(self, lines: list\[str\]) \-\> str:  
  * Generate and return a dialog from lines  
  * CC: 5, 4 decision points \+ 1  
* def get\_embed(self, res: str, out: Any) \-\> tuple\[str, discord.Embed | None\]:  
  * Generates and returns the embed from the result of the input dialog  
  * CC: 7, 6 decision points \+ 1

The impact functionally should be practically none, since we’ve just split the original function into smaller ones by logic, making it easier to test them in the process. There are no practical impactful drawbacks 

### **Function 5:**

The function [update\_embed](https://github.com/python-discord/bot/blob/main/bot/exts/filtering/_ui/filter.py#L250) was initially very complex with a CC of 20 as reported by lizard.  
To improve modularity and clarity it was split into three parts, each of which handles a specific functionality in accordance with clean code principles.

After refactoring [update\_embed](https://github.com/SoffanDD2480/assignment-3-CODE-COVERAGE/blob/refactor-funcs/bot/exts/filtering/_ui/filter.py#L252) itself now has a CC of 7 focusing exclusively in logic and task delegation to the two new functions:

* [\_process\_content\_and\_description](https://github.com/SoffanDD2480/assignment-3-CODE-COVERAGE/blob/refactor-funcs/bot/exts/filtering/_ui/filter.py#L290): Handles content validation, description updates and embedding formatting. CC 10  
* [\_process\_setting\_override](https://github.com/SoffanDD2480/assignment-3-CODE-COVERAGE/blob/refactor-funcs/bot/exts/filtering/_ui/filter.py#L333): Manages settings updates to ensure override values are correctly applied / removed. CC 6

This refactor improves readability and testability by making the code much easier to work with. However, an important consideration is that the total CC of the refactored version is ever so slightly higher with CC 23 as compared to the original CC of 20\. To decompose the complex function into smaller more modular parts some trade-offs need to be made and the benefits clearly outweigh the negatives.

## **Self-assessment: Way of working 2: Electric Boogaloo**

For this assignment, we got a new member, so we had to rethink our way of working. This made us fall back to the ”Principles established” state again, since we need to reestablish our principles and way of working. For example, we still are in the process of establishing how to use GitHub. This clash may also come from the fact that the new member is not new to this course, and has established their own way of working in the previous group, which was different from our way of working. After having done this assignment though, we have been able to agree on how we wanna move forward, although some more discussions are needed. In any way, we have improved since the last time (established some ways of working with GutHub), and we know in which directions we want to follow to improve. We are more or less unanimous about our experience too.

## **Overall experience**

*What are your main take-aways from this project? What did you learn?*

* We have learned how forking works and how to adapt an open source project to run and test on our separate machines.  
* We learned how to get started when contributing to an open source project  
* We learned how to use new tools for analyzing cyclomatic complexity and code coverage, such as lizard for and coverage.py  
* We also learned about the importance of branch coverage 

