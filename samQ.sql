-- Insert Users
INSERT INTO server_user (user_id, name, phone_number, role, email, password, dob, city, state, country, photo_url, type)
VALUES
('user1', 'Admin User', '1234567890', 'admin', 'admin@gmail.com', '12345', '1990-01-01', 'New York', 'NY', 'USA', 'images/krishtec.jpg', 'tech'),
('user2', 'Subadmin User', '2345678901', 'subadmin', 'subadmin@gmail.com', '12345', '1991-02-02', 'Los Angeles', 'CA', 'USA', 'images/krishtec.jpg', 'tech'),
('user3', 'Regular User', '3456789012', 'user', 'user@gmail.com', '12345', '1992-03-03', 'Chicago', 'IL', 'USA', 'images/krishtec.jpg', 'tech');

-- Insert Topics
INSERT INTO server_topic (topic_id, name, created_by_id, created_at, domain_type, tech_type)
VALUES
('topic1', 'Python Programming', 'user1', '2023-01-01 10:00:00', 'tech', 'sw'),
('topic2', 'Web Development', 'user1', '2023-01-02 11:00:00', 'tech', 'sw'),
('topic3', 'Data Science', 'user2', '2023-01-03 12:00:00', 'tech', 'sw');



-- Insert SubTopics for each Topic
INSERT INTO server_subtopic (subtopic_id, name, topic_id_id, created_by_id, created_at)
VALUES
-- Python Programming subtopics
('subtopic1', 'Python Basics', 'topic1', 'user1', '2023-01-01 10:30:00'),
('subtopic2', 'Advanced Python', 'topic1', 'user1', '2023-01-01 11:00:00'),
-- Web Development subtopics
('subtopic3', 'HTML/CSS', 'topic2', 'user1', '2023-01-02 11:30:00'),
('subtopic4', 'JavaScript', 'topic2', 'user1', '2023-01-02 12:00:00'),
-- Data Science subtopics
('subtopic5', 'Data Analysis', 'topic3', 'user2', '2023-01-03 12:30:00'),
('subtopic6', 'Machine Learning', 'topic3', 'user2', '2023-01-03 13:00:00');

-- Insert Learning Materials for each SubTopic
INSERT INTO server_learningmaterial (topic_id_id, subtopic_id_id, content)
VALUES
('topic1', 'subtopic1', 'Introduction to Python syntax and basic concepts.'),
('topic1', 'subtopic2', 'Advanced Python features like decorators and generators.'),
('topic2', 'subtopic3', 'HTML structure and CSS styling basics.'),
('topic2', 'subtopic4', 'JavaScript programming fundamentals.'),
('topic3', 'subtopic5', 'Data analysis with Python and Pandas.'),
('topic3', 'subtopic6', 'Introduction to machine learning algorithms.');

-- Insert Practice Titles for each SubTopic (4 per subtopic)
INSERT INTO server_practice (title_id, topic_id_id, subtopic_id_id, title, duration, attempts)
VALUES
-- Python Basics practices
('practice1', 'topic1', 'subtopic1', 'Python Basics Practice 1', 900, 1),
('practice2', 'topic1', 'subtopic1', 'Python Basics Practice 2', 900, 1),
('practice3', 'topic1', 'subtopic1', 'Python Basics Practice 3', 900, 1),
('practice4', 'topic1', 'subtopic1', 'Python Basics Practice 4', 900, 1),
-- Advanced Python practices
('practice5', 'topic1', 'subtopic2', 'Advanced Python Practice 1', 900, 1),
('practice6', 'topic1', 'subtopic2', 'Advanced Python Practice 2', 900, 1),
('practice7', 'topic1', 'subtopic2', 'Advanced Python Practice 3', 900, 1),
('practice8', 'topic1', 'subtopic2', 'Advanced Python Practice 4', 900, 1),
-- HTML/CSS practices
('practice9', 'topic2', 'subtopic3', 'HTML/CSS Practice 1', 900, 1),
('practice10', 'topic2', 'subtopic3', 'HTML/CSS Practice 2', 900, 1),
('practice11', 'topic2', 'subtopic3', 'HTML/CSS Practice 3', 900, 1),
('practice12', 'topic2', 'subtopic3', 'HTML/CSS Practice 4', 900, 1),
-- JavaScript practices
('practice13', 'topic2', 'subtopic4', 'JavaScript Practice 1', 900, 1),
('practice14', 'topic2', 'subtopic4', 'JavaScript Practice 2', 900, 1),
('practice15', 'topic2', 'subtopic4', 'JavaScript Practice 3', 900, 1),
('practice16', 'topic2', 'subtopic4', 'JavaScript Practice 4', 900, 1),
-- Data Analysis practices
('practice17', 'topic3', 'subtopic5', 'Data Analysis Practice 1', 900, 1),
('practice18', 'topic3', 'subtopic5', 'Data Analysis Practice 2', 900, 1),
('practice19', 'topic3', 'subtopic5', 'Data Analysis Practice 3', 900, 1),
('practice20', 'topic3', 'subtopic5', 'Data Analysis Practice 4', 900, 1),
-- Machine Learning practices
('practice21', 'topic3', 'subtopic6', 'Machine Learning Practice 1', 900, 1),
('practice22', 'topic3', 'subtopic6', 'Machine Learning Practice 2', 900, 1),
('practice23', 'topic3', 'subtopic6', 'Machine Learning Practice 3', 900, 1),
('practice24', 'topic3', 'subtopic6', 'Machine Learning Practice 4', 900, 1);

-- Insert Test Titles for each SubTopic (4 per subtopic)
INSERT INTO server_test (title_id, topic_id_id, subtopic_id_id, title, duration, attempts)
VALUES
-- Python Basics tests
('test1', 'topic1', 'subtopic1', 'Python Basics Test 1', 900, 1),
('test2', 'topic1', 'subtopic1', 'Python Basics Test 2', 900, 1),
('test3', 'topic1', 'subtopic1', 'Python Basics Test 3', 900, 1),
('test4', 'topic1', 'subtopic1', 'Python Basics Test 4', 900, 1),
-- Advanced Python tests
('test5', 'topic1', 'subtopic2', 'Advanced Python Test 1', 900, 1),
('test6', 'topic1', 'subtopic2', 'Advanced Python Test 2', 900, 1),
('test7', 'topic1', 'subtopic2', 'Advanced Python Test 3', 900, 1),
('test8', 'topic1', 'subtopic2', 'Advanced Python Test 4', 900, 1),
-- HTML/CSS tests
('test9', 'topic2', 'subtopic3', 'HTML/CSS Test 1', 900, 1),
('test10', 'topic2', 'subtopic3', 'HTML/CSS Test 2', 900, 1),
('test11', 'topic2', 'subtopic3', 'HTML/CSS Test 3', 900, 1),
('test12', 'topic2', 'subtopic3', 'HTML/CSS Test 4', 900, 1),
-- JavaScript tests
('test13', 'topic2', 'subtopic4', 'JavaScript Test 1', 900, 1),
('test14', 'topic2', 'subtopic4', 'JavaScript Test 2', 900, 1),
('test15', 'topic2', 'subtopic4', 'JavaScript Test 3', 900, 1),
('test16', 'topic2', 'subtopic4', 'JavaScript Test 4', 900, 1),
-- Data Analysis tests
('test17', 'topic3', 'subtopic5', 'Data Analysis Test 1', 900, 1),
('test18', 'topic3', 'subtopic5', 'Data Analysis Test 2', 900, 1),
('test19', 'topic3', 'subtopic5', 'Data Analysis Test 3', 900, 1),
('test20', 'topic3', 'subtopic5', 'Data Analysis Test 4', 900, 1),
-- Machine Learning tests
('test21', 'topic3', 'subtopic6', 'Machine Learning Test 1', 900, 1),
('test22', 'topic3', 'subtopic6', 'Machine Learning Test 2', 900, 1),
('test23', 'topic3', 'subtopic6', 'Machine Learning Test 3', 900, 1),
('test24', 'topic3', 'subtopic6', 'Machine Learning Test 4', 900, 1);

-- Insert Practice Questions (10 per practice)
-- Note: I'll show a sample for 2 practices to keep it manageable, you can replicate for others
INSERT INTO server_practicequestion (question_id, title_id_id, question, correct_option, explanation)
VALUES
-- Practice 1 Questions
('pq1', 'practice1', 'Which of the following is the correct way to declare a variable in Python?', 1, 'In Python, variables are declared by simply assigning a value. No special keyword is needed.'),
('pq2', 'practice1', 'What is the output of print(2 + 3 * 4)?', 3, 'Multiplication has higher precedence than addition, so 3*4=12, then 2+12=14.'),
('pq3', 'practice1', 'Which of these is NOT a Python data type?', 4, 'Python has int, float, and str types, but "char" is not a separate type in Python.'),
('pq4', 'practice1', 'What does the len() function do?', 2, 'The len() function returns the number of items in an object like a string or list.'),
('pq5', 'practice1', 'How do you start a single-line comment in Python?', 1, 'Single-line comments in Python start with a # symbol.'),
('pq6', 'practice1', 'Which operator is used for exponentiation in Python?', 4, 'The ** operator is used for exponentiation in Python.'),
('pq7', 'practice1', 'What is the output of print("Hello"[1])?', 2, 'String indices start at 0, so index 1 is the second character "e".'),
('pq8', 'practice1', 'Which of these collections is ordered and changeable?', 1, 'Lists are ordered and changeable, while tuples are immutable.'),
('pq9', 'practice1', 'How do you create a tuple in Python?', 3, 'Tuples are created with parentheses, or just commas for single-item tuples.'),
('pq10', 'practice1', 'Which method removes the last item from a list?', 4, 'The pop() method removes and returns the last item by default.'),

-- Practice 2 Questions
('pq11', 'practice2', 'What is the output of print(10 / 3)?', 3, 'The / operator performs floating-point division in Python 3.'),
('pq12', 'practice2', 'Which of these is the correct way to import a module?', 1, 'The import statement is used to import modules.'),
('pq13', 'practice2', 'What does the range(5) function return?', 2, 'range(5) generates numbers from 0 to 4 (5 numbers total).'),
('pq14', 'practice2', 'Which keyword is used to define a function?', 4, 'The def keyword is used to define functions in Python.'),
('pq15', 'practice2', 'What is the output of print("Python".upper())?', 1, 'The upper() method converts all characters to uppercase.'),
('pq16', 'practice2', 'Which of these is a valid dictionary declaration?', 3, 'Dictionaries are declared with curly braces and key:value pairs.'),
('pq17', 'practice2', 'What does the append() method do?', 2, 'append() adds an item to the end of a list.'),
('pq18', 'practice2', 'Which operator checks if two values are equal?', 1, 'The == operator checks for equality in Python.'),
('pq19', 'practice2', 'What is the output of print(bool(""))?', 4, 'Empty strings are considered False in boolean context.'),
('pq20', 'practice2', 'Which of these is NOT a Python loop?', 3, 'Python has for and while loops, but no "do-while" loop.');

-- Insert Practice Options for each Question
INSERT INTO server_practiceoption (option_id, question_id_id, option1, option2, option3, option4)
VALUES
-- Practice 1 Options
('po1', 'pq1', 'x = 5', 'var x = 5', 'int x = 5', 'let x = 5'),
('po2', 'pq1', '10', '14', '20', '24'),
('po3', 'pq1', 'int', 'float', 'str', 'char'),
('po4', 'pq1', 'Returns the length of a string', 'Returns the number of items in an object', 'Returns the size of a file', 'Returns the memory usage'),
('po5', 'pq1', '# This is a comment', '// This is a comment', '/* This is a comment */', '-- This is a comment'),
('po6', 'pq1', '^', '%', '//', '**'),
('po7', 'pq1', 'H', 'e', 'l', 'o'),
('po8', 'pq1', 'List', 'Tuple', 'Set', 'Dictionary'),
('po9', 'pq1', 'x = [1, 2, 3]', 'x = {1, 2, 3}', 'x = (1, 2, 3)', 'x = {"a":1, "b":2}'),
('po10', 'pq1', 'remove()', 'delete()', 'discard()', 'pop()'),

-- Practice 2 Options
('po11', 'pq11', '3', '3.333', '3.3333333333333335', '3.0'),
('po12', 'pq11', 'import math', 'include math', 'require math', 'using math'),
('po13', 'pq11', '[0,1,2,3,4,5]', 'range(0,5)', '[1,2,3,4,5]', 'range(1,6)'),
('po14', 'pq11', 'function', 'func', 'fn', 'def'),
('po15', 'pq11', 'PYTHON', 'python', 'Python', 'Error'),
('po16', 'pq11', 'x = [1:"one", 2:"two"]', 'x = (1:"one", 2:"two")', 'x = {1:"one", 2:"two"}', 'x = <1:"one", 2:"two">'),
('po17', 'pq11', 'Removes an item', 'Adds an item to the end', 'Adds an item to the beginning', 'Reverses the list'),
('po18', 'pq11', '==', '=', '===', 'equals'),
('po19', 'pq11', 'True', 'None', 'Error', 'False'),
('po20', 'pq11', 'for', 'while', 'do-while', 'nested');

-- Insert Test Questions (10 per test)
-- Sample for 2 tests
INSERT INTO server_testquestion (question_id, title_id_id, question, correct_option, explanation)
VALUES
-- Test 1 Questions
('tq1', 'test1', 'What is the correct syntax to output "Hello World" in Python?', 1, 'The print() function is used to output text in Python.'),
('tq2', 'test1', 'How do you insert COMMENTS in Python code?', 2, 'Single-line comments start with # in Python.'),
('tq3', 'test1', 'Which one is NOT a legal variable name?', 4, 'Variable names cannot start with a number.'),
('tq4', 'test1', 'What is the correct file extension for Python files?', 3, 'Python files typically use the .py extension.'),
('tq5', 'test1', 'How do you create a variable with the numeric value 5?', 1, 'Variables are assigned with the = operator.'),
('tq6', 'test1', 'What is the correct syntax to output the type of a variable or object in Python?', 4, 'The type() function returns the type of an object.'),
('tq7', 'test1', 'What is the output of print(10 == "10")?', 4, 'The == operator compares value and type, which are different here.'),
('tq8', 'test1', 'Which method can be used to remove any whitespace from both the beginning and the end of a string?', 3, 'The strip() method removes leading and trailing whitespace.'),
('tq9', 'test1', 'Which operator can be used to compare two values?', 2, 'The == operator compares two values for equality.'),
('tq10', 'test1', 'Which of these collections defines a LIST?', 1, 'Lists are defined with square brackets [] in Python.'),

-- Test 2 Questions
('tq11', 'test2', 'Which method can be used to return a string in upper case letters?', 2, 'The upper() method converts a string to uppercase.'),
('tq12', 'test2', 'Which statement is used to stop a loop?', 3, 'The break statement stops the loop execution.'),
('tq13', 'test2', 'Which of these is a correct dictionary declaration?', 4, 'Dictionaries use curly braces with key:value pairs.'),
('tq14', 'test2', 'Which collection is ordered, changeable, and allows duplicate members?', 1, 'Lists have all these characteristics.'),
('tq15', 'test2', 'How do you start writing an if statement in Python?', 2, 'The if statement starts with the if keyword.'),
('tq16', 'test2', 'Which keyword is used to create a function?', 3, 'The def keyword defines a function in Python.'),
('tq17', 'test2', 'What is the output of print(bool(0))?', 4, '0 is considered False in boolean context.'),
('tq18', 'test2', 'What is the output of print("Hello" + "World")?', 1, 'The + operator concatenates strings.'),
('tq19', 'test2', 'Which operator is used to multiply numbers?', 2, 'The * operator is used for multiplication.'),
('tq20', 'test2', 'Which of these is a correct way to create a set?', 3, 'Sets are created with curly braces {}.');

-- Insert Test Options for each Question
INSERT INTO server_testoption (option_id, question_id_id, option1, option2, option3, option4)
VALUES
-- Test 1 Options
('to1', 'tq1', 'print("Hello World")', 'echo "Hello World"', 'printf("Hello World")', 'console.log("Hello World")'),
('to2', 'tq1', '# This is a comment', '// This is a comment', '/* This is a comment */', '-- This is a comment'),
('to3', 'tq1', 'myvar', '_myvar', 'MyVar', '2myvar'),
('to4', 'tq1', '.pyth', '.pt', '.py', '.python'),
('to5', 'tq1', 'x = 5', 'x := 5', 'x -> 5', 'int x = 5'),
('to6', 'tq1', 'print(typeOf(x))', 'print(typeof x)', 'print(typeOf x)', 'print(type(x))'),
('to7', 'tq1', 'True', '10', '"10"', 'False'),
('to8', 'tq1', 'trim()', 'ptrim()', 'strip()', 'cut()'),
('to9', 'tq1', '=', '==', '<>', '><'),
('to10', 'tq1', '["apple", "banana", "cherry"]', '{"apple", "banana", "cherry"}', '("apple", "banana", "cherry")', '{"name": "apple", "color": "red"}'),

-- Test 2 Options
('to11', 'tq11', 'toUpperCase()', 'upper()', 'uppercase()', 'toUpper()'),
('to12', 'tq11', 'return', 'exit', 'break', 'stop'),
('to13', 'tq11', '{"name": "apple", "color": "red"}', '["apple", "banana", "cherry"]', '("apple", "banana", "cherry")', '{"apple", "banana", "cherry"}'),
('to14', 'tq11', 'List', 'Tuple', 'Set', 'Dictionary'),
('to15', 'tq11', 'if x > y:', 'if (x > y)', 'if x > y then', 'if x > y {'),
('to16', 'tq11', 'function', 'fun', 'def', 'define'),
('to17', 'tq11', 'True', 'None', 'Error', 'False'),
('to18', 'tq11', 'HelloWorld', 'Hello World', '"Hello"+"World"', 'Error'),
('to19', 'tq11', 'x', '%', '*', '#'),
('to20', 'tq11', '{"name": "apple", "color": "red"}', '["apple", "banana", "cherry"]', '{"apple", "banana", "cherry"}', '("apple", "banana", "cherry")');

