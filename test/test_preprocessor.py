from stack_under_flow.model import Preprocessor

class TestPreprocessor:

    data_for_test_crawler = [
        """
        <p>To understand what <code>yield</code> does, you must understand what <em>generators</em> are. And before you can understand generators, you must understand <em>iterables</em>.</p>

    <h2>Iterables</h2>

    <p>When you create a list, you can read its items one by one. Reading its items one by one is called iteration:</p>

    <pre><code>&gt;&gt;&gt; mylist = [1, 2, 3]
    &gt;&gt;&gt; for i in mylist:
    ...    print(i)
    1
    2
    3
    </code></pre>

    <p><code>mylist</code> is an <em>iterable</em>. When you use a list comprehension, you create a list, and so an iterable:</p>

    <pre><code>&gt;&gt;&gt; mylist = [x*x for x in range(3)]
    &gt;&gt;&gt; for i in mylist:
    ...    print(i)
    0
    1
    4
    </code></pre>

    <p>Everything you can use "<code>for... in...</code>" on is an iterable; <code>lists</code>, <code>strings</code>, files...</p>

    <p>These iterables are handy because you can read them as much as you wish, but you store all the values in memory and this is not always what you want when you have a lot of values.</p>

    <h2>Generators</h2>

    <p>Generators are iterators, a kind of iterable <strong>you can only iterate over once</strong>. Generators do not store all the values in memory, <strong>they generate the values on the fly</strong>:</p>

    <pre><code>&gt;&gt;&gt; mygenerator = (x*x for x in range(3))
    &gt;&gt;&gt; for i in mygenerator:
    ...    print(i)
    0
    1
    4
    </code></pre>

    <p>It is just the same except you used <code>()</code> instead of <code>[]</code>. BUT, you <strong>cannot</strong> perform <code>for i in mygenerator</code> a second time since generators can only be used once: they calculate 0, then forget about it and calculate 1, and end calculating 4, one by one.</p>

    <h2>Yield</h2>

    <p><code>yield</code> is a keyword that is used like <code>return</code>, except the function will return a generator.</p>

    <pre><code>&gt;&gt;&gt; def createGenerator():
    ...    mylist = range(3)
    ...    for i in mylist:
    ...        yield i*i
    ...
    &gt;&gt;&gt; mygenerator = createGenerator() # create a generator
    &gt;&gt;&gt; print(mygenerator) # mygenerator is an object!
    &lt;generator object createGenerator at 0xb7555c34&gt;
    &gt;&gt;&gt; for i in mygenerator:
    ...     print(i)
    0
    1
    4
    </code></pre>

    <p>Here it's a useless example, but it's handy when you know your function will return a huge set of values that you will only need to read once.</p>

    <p>To master <code>yield</code>, you must understand that <strong>when you call the function, the code you have written in the function body does not run.</strong> The function only returns the generator object, this is a bit tricky :-)</p>

    <p>Then, your code will continue from where it left off each time <code>for</code> uses the generator.</p>

    <p>Now the hard part:</p>

    <p>The first time the <code>for</code> calls the generator object created from your function, it will run the code in your function from the beginning until it hits <code>yield</code>, then it'll return the first value of the loop. Then, each other call will run the loop you have written in the function one more time, and return the next value until there is no value to return.</p>

    <p>The generator is considered empty once the function runs, but does not hit <code>yield</code> anymore. It can be because the loop had come to an end, or because you do not satisfy an <code>"if/else"</code> anymore.</p>

    <hr>

    <h2>Your code explained</h2>

    <p><em>Generator:</em></p>

    <pre><code># Here you create the method of the node object that will return the generator
    def _get_child_candidates(self, distance, min_dist, max_dist):

        # Here is the code that will be called each time you use the generator object:

        # If there is still a child of the node object on its left
        # AND if the distance is ok, return the next child
        if self._leftchild and distance - max_dist &lt; self._median:
            yield self._leftchild

        # If there is still a child of the node object on its right
        # AND if the distance is ok, return the next child
        if self._rightchild and distance + max_dist &gt;= self._median:
            yield self._rightchild

        # If the function arrives here, the generator will be considered empty
        # there is no more than two values: the left and the right children
    </code></pre>

    <p><em>Caller:</em></p>

    <pre><code># Create an empty list and a list with the current object reference
    result, candidates = list(), [self]

    # Loop on candidates (they contain only one element at the beginning)
    while candidates:

        # Get the last candidate and remove it from the list
        node = candidates.pop()

        # Get the distance between obj and the candidate
        distance = node._get_dist(obj)

        # If distance is ok, then you can fill the result
        if distance &lt;= max_dist and distance &gt;= min_dist:
            result.extend(node._values)

        # Add the children of the candidate in the candidate's list
        # so the loop will keep running until it will have looked
        # at all the children of the children of the children, etc. of the candidate
        candidates.extend(node._get_child_candidates(distance, min_dist, max_dist))

    return result
    </code></pre>

    <p>This code contains several smart parts:</p>

    <ul>
    <li><p>The loop iterates on a list, but the list expands while the loop is being iterated :-) It's a concise way to go through all these nested data even if it's a bit dangerous since you can end up with an infinite loop. In this case, <code>candidates.extend(node._get_child_candidates(distance, min_dist, max_dist))</code> exhaust all the values of the generator, but <code>while</code> keeps creating new generator objects which will produce different values from the previous ones since it's not applied on the same node.</p></li>
    <li><p>The <code>extend()</code> method is a list object method that expects an iterable and adds its values to the list.</p></li>
    </ul>

    <p>Usually we pass a list to it:</p>

    <pre><code>&gt;&gt;&gt; a = [1, 2]
    &gt;&gt;&gt; b = [3, 4]
    &gt;&gt;&gt; a.extend(b)
    &gt;&gt;&gt; print(a)
    [1, 2, 3, 4]
    </code></pre>

    <p>But in your code, it gets a generator, which is good because:</p>

    <ol>
    <li>You don't need to read the values twice.</li>
    <li>You may have a lot of children and you don't want them all stored in memory.</li>
    </ol>

    <p>And it works because Python does not care if the argument of a method is a list or not. Python expects iterables so it will work with strings, lists, tuples, and generators! This is called duck typing and is one of the reasons why Python is so cool. But this is another story, for another question...</p>

    <p>You can stop here, or read a little bit to see an advanced use of a generator:</p>

    <h2>Controlling a generator exhaustion</h2>

    <pre><code>&gt;&gt;&gt; class Bank(): # Let's create a bank, building ATMs
    ...    crisis = False
    ...    def create_atm(self):
    ...        while not self.crisis:
    ...            yield "$100"
    &gt;&gt;&gt; hsbc = Bank() # When everything's ok the ATM gives you as much as you want
    &gt;&gt;&gt; corner_street_atm = hsbc.create_atm()
    &gt;&gt;&gt; print(corner_street_atm.next())
    $100
    &gt;&gt;&gt; print(corner_street_atm.next())
    $100
    &gt;&gt;&gt; print([corner_street_atm.next() for cash in range(5)])
    ['$100', '$100', '$100', '$100', '$100']
    &gt;&gt;&gt; hsbc.crisis = True # Crisis is coming, no more money!
    &gt;&gt;&gt; print(corner_street_atm.next())
    &lt;type 'exceptions.StopIteration'&gt;
    &gt;&gt;&gt; wall_street_atm = hsbc.create_atm() # It's even true for new ATMs
    &gt;&gt;&gt; print(wall_street_atm.next())
    &lt;type 'exceptions.StopIteration'&gt;
    &gt;&gt;&gt; hsbc.crisis = False # The trouble is, even post-crisis the ATM remains empty
    &gt;&gt;&gt; print(corner_street_atm.next())
    &lt;type 'exceptions.StopIteration'&gt;
    &gt;&gt;&gt; brand_new_atm = hsbc.create_atm() # Build a new one to get back in business
    &gt;&gt;&gt; for cash in brand_new_atm:
    ...    print cash
    $100
    $100
    $100
    $100
    $100
    $100
    $100
    $100
    $100
    ...
    </code></pre>

    <p><strong>Note:</strong> For Python 3, use<code>print(corner_street_atm.__next__())</code> or <code>print(next(corner_street_atm))</code></p>

    <p>It can be useful for various things like controlling access to a resource.</p>

    <h2>Itertools, your best friend</h2>

    <p>The itertools module contains special functions to manipulate iterables. Ever wish to duplicate a generator?
    Chain two generators? Group values in a nested list with a one-liner? <code>Map / Zip</code> without creating another list?</p>

    <p>Then just <code>import itertools</code>.</p>

    <p>An example? Let's see the possible orders of arrival for a four-horse race:</p>

    <pre><code>&gt;&gt;&gt; horses = [1, 2, 3, 4]
    &gt;&gt;&gt; races = itertools.permutations(horses)
    &gt;&gt;&gt; print(races)
    &lt;itertools.permutations object at 0xb754f1dc&gt;
    &gt;&gt;&gt; print(list(itertools.permutations(horses)))
    [(1, 2, 3, 4),
     (1, 2, 4, 3),
     (1, 3, 2, 4),
     (1, 3, 4, 2),
     (1, 4, 2, 3),
     (1, 4, 3, 2),
     (2, 1, 3, 4),
     (2, 1, 4, 3),
     (2, 3, 1, 4),
     (2, 3, 4, 1),
     (2, 4, 1, 3),
     (2, 4, 3, 1),
     (3, 1, 2, 4),
     (3, 1, 4, 2),
     (3, 2, 1, 4),
     (3, 2, 4, 1),
     (3, 4, 1, 2),
     (3, 4, 2, 1),
     (4, 1, 2, 3),
     (4, 1, 3, 2),
     (4, 2, 1, 3),
     (4, 2, 3, 1),
     (4, 3, 1, 2),
     (4, 3, 2, 1)]
    </code></pre>

    <h2>Understanding the inner mechanisms of iteration</h2>

    <p>Iteration is a process implying iterables (implementing the <code>__iter__()</code> method) and iterators (implementing the <code>__next__()</code> method).
    Iterables are any objects you can get an iterator from. Iterators are objects that let you iterate on iterables.</p>

    <p>There is more about it in this article about <a href="http://effbot.org/zone/python-for-statement.htm" rel="noreferrer">how <code>for</code> loops work</a>.</p>
        """,
        """
        <p>Yes, it was <a href="https://mail.python.org/pipermail/python-dev/2005-September/056846.html" rel="noreferrer" title="[Python-Dev] Conditional Expression Resolution">added</a> in version 2.5. The expression syntax is:</p>

    <pre><code>a if condition else b
    </code></pre>

    <p>First <code>condition</code> is evaluated, then exactly one of either <code>a</code> or <code>b</code> is evaluated and returned based on the <a href="https://en.wikipedia.org/wiki/Boolean_data_type" rel="noreferrer" title="Boolean data type">Boolean</a> value of <code>condition</code>. If <code>condition</code> evaluates to <code>True</code>, then <code>a</code> is evaluated and returned but <code>b</code> is ignored, or else when <code>b</code> is evaluated and returned but <code>a</code> is ignored.</p>

    <p>This allows short-circuiting because when <code>condition</code> is true only <code>a</code> is evaluated and <code>b</code> is not evaluated at all, but when <code>condition</code> is false only <code>b</code> is evaluated and <code>a</code> is not evaluated at all.</p>

    <p>For example:</p>

    <pre><code>&gt;&gt;&gt; 'true' if True else 'false'
    'true'
    &gt;&gt;&gt; 'true' if False else 'false'
    'false'
    </code></pre>

    <p>Note that conditionals are an <em>expression</em>, not a <em>statement</em>. This means you can't use assignment statements or <code>pass</code> or other <strong>statements</strong> within a conditional <strong>expression</strong>:</p>

    <pre><code>&gt;&gt;&gt; pass if False else x = 3
      File "&lt;stdin&gt;", line 1
        pass if False else x = 3
              ^
    SyntaxError: invalid syntax
    </code></pre>

    <p>You can, however, use conditional expressions to assign a variable like so:</p>

    <pre><code>x = a if True else b
    </code></pre>

    <p>Think of the conditional expression as switching between two values. It is very useful when you're in a 'one value or another' situation, it but doesn't do much else.</p>

    <p>If you need to use statements, you have to use a normal <code>if</code> <strong>statement</strong> instead of a conditional <strong>expression</strong>.</p>

    <hr>

    <p>Keep in mind that it's frowned upon by some Pythonistas for several reasons:</p>

    <ul>
    <li>The order of the arguments is different from those of the classic <code>condition ? a : b</code> ternary operator from many other languages (such as C, C++, Go, Perl, Ruby, Java, Javascript, etc.), which may lead to bugs when people unfamiliar with Python's "surprising" behaviour use it (they may reverse the argument order).</li>
    <li>Some find it "unwieldy", since it goes contrary to the normal flow of thought (thinking of the condition first and then the effects).</li>
    <li>Stylistic reasons. (Although the 'inline <code>if</code>' can be <em>really</em> useful, and make your script more concise, it really does complicate your code)</li>
    </ul>

    <p>If you're having trouble remembering the order, then remember that when read aloud, you (almost) say what you mean. For example, <code>x = 4 if b &gt; 8 else 9</code> is read aloud as <code>x will be 4 if b is greater than 8 otherwise 9</code>.</p>

    <p>Official documentation:     </p>

    <ul>
    <li><a href="https://docs.python.org/3/reference/expressions.html#conditional-expressions" rel="noreferrer" title="Conditional expressions">Conditional expressions</a></li>
    <li><a href="https://docs.python.org/3.3/faq/programming.html#is-there-an-equivalent-of-c-s-ternary-operator" rel="noreferrer" title="Is there an equivalent of C’s ”?:” ternary operator?">Is there an equivalent of C’s ”?:” ternary operator?</a></li>
    </ul>
        """
    ]

    def test_transform(self):
        preprocessor = Preprocessor(
            word2vec_model_src="/Users/sachaizadi/Documents/Projets/stack_under_flow/stack_under_flow/model/word2vec.model"
        )

        x_str = preprocessor.transform(self.data_for_test_crawler, vectorize=False)
        x_not_reduced = preprocessor.transform(self.data_for_test_crawler, reducer=None)
        x = preprocessor.transform(self.data_for_test_crawler)

        assert len(x_str) == len(x_not_reduced) == len(x)
        assert len(x_str[0]) == len(x_not_reduced[0]) == x[0].shape[0]
        assert x_not_reduced[0][0].shape[1] == x[0][0].shape[0]
