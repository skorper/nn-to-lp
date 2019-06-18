# nn-to-lp


----
## usage
1. Requires Python 3 and various ML libraries
2. How to run:

`python main.py`

3. If "Unable to confirm model." is returned, run again. This means that the model was not reproducible by this algorithm. Depending on the complexity of the neural network this may happen multiple times, because I only allow this code to continue if it's perfectly (100%) reproducible). 

4. In order to change the size of the neural network (number of layers/nodes in hidden layers) modify line 16.

`hidden_layers = (2, 2) #10, 10, 10 would be 3 layers of 10`

5. Lines 12 - 13 can be replaced by another dataset other than iris. 

```
X = iris.data # Your training data here
y = iris.target # Your training target here
```

6. This generates a logic program tst.lp and input.lp. These are already tested in the code but can also be run through clingo if desired. 

7. There are other methods of testing the rule generation, all files that begin with test_* are testing some functionality of the rule generation. 

---

## Ideas for improvement

1. Implement other activation functions.
2. Improve code style by re-writing in a more pythonic way (removing loop nesting), and ensure all matrix/vector operations use numpy for faster calculation. This would be a top priority IMO because the looping is abysmal.
