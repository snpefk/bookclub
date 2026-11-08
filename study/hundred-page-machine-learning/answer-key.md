# Answer key — Chapters 1–4

Spoilers: finish the test before reading. Essay questions require manual self-assessment.

## Chapter 1 — Introduction

### 1. Learning from examples

Which activity best matches the chapter's definition of machine learning?

**Answer:** Building a statistical model from examples to solve a practical problem

Machine learning uses a dataset to algorithmically build a statistical model for a practical task. Source: section 1.1.

### 2. Learning settings

Match each dataset or interaction setting to its learning type.

**Answer:** Emails with spam labels → Supervised; Unlabeled customer vectors to group → Unsupervised; A few labeled images plus many unlabeled images → Semi-supervised; An agent taking actions and receiving rewards → Reinforcement

The distinctions concern available supervision and, in reinforcement learning, sequential interaction and reward. Source: section 1.2.

### 3. Consistent features

In a dataset of people, feature position 2 contains weight in kilograms. What must be true of position 2 in other examples?

**Answer:** It must represent the same kind of information with the same meaning and units

A coordinate must have consistent semantics across examples; its value can differ. Source: section 1.2.1.

### 4. Unsupervised output

Which task is an example of dimensionality reduction?

**Answer:** Mapping each input vector to a vector with fewer features

Dimensionality reduction transforms the representation without requiring target labels. Source: section 1.2.2.

### 5. Why unlabeled data helps

Why might adding unlabeled examples improve a semi-supervised model?

**Answer:** They can reveal structure in the input distribution that helps learn from the labeled examples

Additional input-distribution information can help, but improvement is not guaranteed. Source: section 1.2.3.

### 6. Policy

What does a reinforcement-learning policy map, in the chapter's description?

**Answer:** A state representation to an action

A policy chooses actions based on state, aiming at a long-term reward objective rather than merely an immediate payoff. Source: section 1.2.4.

### 7. Bag of words dimension

A binary bag-of-words dictionary contains 20,000 words. A dataset contains 10,000 emails. How many features does EACH email vector have?

**Answer:** 20000

Dimensionality is the dictionary size; the number of examples is a separate quantity. Source: section 1.3.

### 8. Binary word presence

In the chapter's binary bag-of-words representation, an email contains the dictionary word "offer" five times. What is that word's feature value?

**Answer:** 1

This particular representation records presence, not frequency or word order. Source: section 1.3.

### 9. Training versus prediction

Which sequence describes prediction with an already trained spam SVM?

**Answer:** Apply the training-time feature encoding, compute the learned linear score, and take its sign

Training finds the parameters. Prediction applies the fixed model to a consistently encoded new input. Source: section 1.3.

### 10. SVM sign calculation

Use the chapter's convention: score is w dot x minus b. With w = [2, -1], x = [3, 1], and b = 2, what label (+1 or -1) is predicted?

**Answer:** 1

The score is 2*3 - 1*1 - 2 = 3, so its sign is +1. A score exactly zero would require a tie convention. Source: section 1.3.

### 11. Hyperplane dimension

In a 12-dimensional input space, how many dimensions does a nondegenerate linear decision hyperplane have?

**Answer:** 11

One independent linear equality reduces the dimension by one. Source: section 1.3.

### 12. Hard-margin constraint

Which is the compact hard-margin SVM constraint for every training example in the chapter's notation?

**Answer:** y_i * (w dot x_i - b) >= 1

For labels +1 and -1, this enforces both correct classification and a score margin of at least one. Source: section 1.3.

### 13. Margin width

For the canonical hard-margin constraints, the distance between the two supporting hyperplanes is 2 / ||w||. If ||w|| is 4, what is the full margin width?

**Answer:** 0.5

The width is 2/4 = 0.5. Minimizing the norm increases this margin subject to the constraints. Source: section 1.3.

### 14. Beyond accuracy

Select TWO practical considerations the chapter gives in addition to predictive accuracy.

**Answer:** Model-building time; Prediction-processing time

Training cost and inference latency can justify choosing a somewhat less accurate model. Source: section 1.3.

### 15. Generalization assumptions

Which situation most directly supports the chapter's intuition about performance on new data?

**Answer:** Training and future examples are independently sampled using the same data-generating procedure

Comparable, representative sampling supports generalization; it is not an unconditional guarantee. Source: section 1.4.

### 16. Perfect separation is not always possible

Why might no hyperplane perfectly separate the training classes?

**Answer:** Noise, label errors, outliers, or genuinely nonlinear class structure

The chapter introduces limits of the simple hard-margin linear setup, developed further in Chapter 3. Source: section 1.3.

### 17. Sampling shift diagnosis

A spam model is trained on personal English emails, then deployed on corporate messages in another language. Explain why high training accuracy may not transfer.

**Answer:** Use the rubric below.

Self-assessment: mark correct only if your answer includes ALL of the following. The training and deployment distributions differ; the learned features or boundary may not describe the new population; training accuracy alone does not establish performance on that population. Source: section 1.4.

### 18. Learning pipeline

Describe an end-to-end supervised spam-detection pipeline, distinguishing training from prediction.

**Answer:** Use the rubric below.

Self-assessment: mark correct only if your answer includes ALL of the following. Collect input-label pairs; choose a consistent feature encoding; train to learn model parameters; encode unseen emails the same way and apply the learned model without using their unknown labels. Source: section 1.3.

## Chapter 2 — Notation and Definitions

### 1. Data structures

Match each mathematical object to its description.

**Answer:** Scalar → One numerical value; Vector → An ordered list of numerical values; Matrix → A rectangular array of numerical values; Set → An unordered collection of unique elements

Ordering matters for vectors, but not for sets; repeated elements do not increase set cardinality. Source: section 2.1.1.

### 2. Indexed feature notation

What does x_i^(j) denote in the book?

**Answer:** Feature j of example i

The parenthesized superscript is an index, not an exponent. Source: section 2.1.1.

### 3. Sigma

Compute the sum of 2i for i from 1 through 4.

**Answer:** 20

2 + 4 + 6 + 8 = 20. Source: section 2.1.2.

### 4. Pi

Compute the product of i for i from 1 through 4.

**Answer:** 24

1 * 2 * 3 * 4 = 24. Source: section 2.1.3.

### 5. Set operations

Let A contain 1, 3, 5 and B contain 3, 4. Which is their intersection?

**Answer:** The set containing only 3

Intersection retains elements present in both sets; union would contain 1, 3, 4, 5. Source: section 2.1.4.

### 6. Derived set

Let S contain 1, 3, 4, 5. Form T from x squared for x in S with x > 3. What is the sum of the elements of T?

**Answer:** 41

Only 4 and 5 satisfy the condition; T contains 16 and 25, whose sum is 41. Source: section 2.1.4.

### 7. Dot product

Compute the dot product of [2, -1, 3] and [4, 5, 0].

**Answer:** 3

2*4 + (-1)*5 + 3*0 = 3. A dot product is a scalar. Source: section 2.1.5.

### 8. Matrix-vector shape

W has 3 rows and 2 columns. x is a column vector with 2 entries. What is the shape of Wx?

**Answer:** A column vector with 3 entries

The inner dimensions match, and each row of W produces one output entry. Source: section 2.1.5.

### 9. Arg max

For inputs a, b, c, a function returns 2, 7, 4 respectively. What does arg max return?

**Answer:** b

arg max returns a maximizing input; max returns the output value 7. Source: section 2.1.7.

### 10. Local versus global

Which statement about a local minimum is correct?

**Answer:** It is no higher than nearby values, but a lower value may exist elsewhere

Local optimality concerns a neighborhood, while global optimality concerns the full domain. Source: section 2.1.6.

### 11. Chain rule

For F(x) = (3x + 1)^2, what is F'(2)?

**Answer:** 42

F'(x) = 2(3x+1)*3, so F'(2) = 42. Source: section 2.1.9.

### 12. Gradient

For f(u,v) = 3u + 2v + 7, what is the gradient with coordinates ordered u, v?

**Answer:** [3, 2]

Take one partial derivative per coordinate, holding the other coordinate constant. Source: section 2.1.9.

### 13. Density versus probability

A random variable has a continuous density. Which statement is correct?

**Answer:** An interval probability is an area under the density; a single point has probability zero

A density is not a probability mass function. Its integral is one; its height can exceed one. Source: section 2.2.

### 14. Expectation

X takes value 0 with probability 0.25 and value 4 with probability 0.75. What is E[X]?

**Answer:** 3

The probability-weighted average is 0*0.25 + 4*0.75 = 3. Source: section 2.2.

### 15. Variance

X takes 0 and 2, each with probability 0.5. What is its variance?

**Answer:** 1

Its mean is 1, so variance is 0.5*(0-1)^2 + 0.5*(2-1)^2 = 1. Source: section 2.2.

### 16. Unbiased does not mean exact

What does it mean for an estimator of a quantity to be unbiased?

**Answer:** Its expectation over repeated samples equals the true quantity

An individual estimate can be wrong even when the estimator is unbiased. Source: section 2.3.

### 17. Sample mean

For the observed sample 2, 4, 9, what is the sample mean?

**Answer:** 5

(2+4+9)/3 = 5; the sample mean is an unbiased estimator of the population mean under the usual sampling assumptions. Source: section 2.3.

### 18. Bayes calculation

P(A) = 0.2, P(B given A) = 0.6, and P(B) = 0.3. What is P(A given B)?

**Answer:** 0.4

Bayes' rule gives 0.6*0.2/0.3 = 0.4. Source: section 2.4.

### 19. Bayesian terms

Match each Bayesian term to its meaning.

**Answer:** Prior → Belief about parameters before the current data; Likelihood → Data probability or density as a function of parameters; Posterior → Belief about parameters after conditioning on data; MAP estimate → Parameter value maximizing the posterior

Posterior is proportional to likelihood times prior; evidence normalizes it. Source: section 2.5.

### 20. Parameters and hyperparameters

Select TWO hyperparameters rather than fitted model coefficients.

**Answer:** The chosen maximum depth of a decision tree; The chosen k in k-nearest neighbors

Hyperparameters control the learning setup; coefficients and intercept are fitted within that setup. Hyperparameters can themselves be selected using validation. Source: section 2.6.

### 21. Prediction targets

Match each target type to the appropriate task.

**Answer:** Spam or not spam → Binary classification; One of cat, dog, horse → Multiclass classification; A house price in euros → Regression; One of three numeric class codes → Multiclass classification, despite numeric encoding

Task type depends on target meaning, not whether its storage format is numeric. Source: section 2.7.

### 22. Instance-based learning

Why does ordinary kNN need the training examples when predicting?

**Answer:** Its predictions depend on finding nearby stored examples and their labels

The stored examples are central to its instance-based prediction procedure. Source: section 2.8.

### 23. Deep representation

What distinguishes the deep-learning description in this chapter?

**Answer:** Multiple learned layers, with later layers receiving representations produced by preceding layers

Depth concerns successive learned transformations, not merely dataset size or training duration. Source: section 2.9.

### 24. Bayesian sequential update

Explain how to update beliefs about a fixed parameter after two conditionally independent observations.

**Answer:** Use the rubric below.

Self-assessment: mark correct only if your answer includes ALL of the following. Start with a prior; multiply by the first observation's likelihood and normalize; use that posterior as the next prior; multiply by the second likelihood and normalize. Equivalently the final posterior is proportional to the original prior times both likelihoods. Do not count the prior twice. Source: section 2.5.

## Chapter 3 — Fundamental Algorithms

### 1. Linear prediction

For f(x) = w dot x + b, w = [2, -1], x = [3, 4], b = 5, what is f(x)?

**Answer:** 7

2*3 - 1*4 + 5 = 7. Source: section 3.1.1.

### 2. MSE

A model predicts 1 and 5 for targets 3 and 4. What is the mean squared error?

**Answer:** 2.5

The squared errors are 4 and 1; their average is 2.5. Source: section 3.1.2.

### 3. Why square errors

Which is a useful property of squared-error loss compared with absolute-error loss?

**Answer:** It is differentiable everywhere and increasingly penalizes larger residual magnitudes

Squaring is smooth and magnifies large errors. That also makes it sensitive to large residuals. Source: section 3.1.2.

### 4. Overfitting

Which outcome is characteristic of overfitting?

**Answer:** Very low training error but substantially worse error on representative unseen examples

Fitting training peculiarities does not necessarily capture patterns that persist in new data. Source: section 3.1.2.

### 5. Logistic task

Despite its name, what task does binary logistic regression solve?

**Answer:** Classification

Its sigmoid output can be interpreted as a positive-class probability and thresholded into a class. Source: section 3.2.

### 6. Sigmoid at zero

What is sigmoid(0), where sigmoid(z) = 1/(1+exp(-z))?

**Answer:** 0.5

exp(0)=1, so the result is 1/2. Source: section 3.2.1.

### 7. Threshold is a choice

A logistic model assigns positive-class probability 0.6. What happens if the threshold is raised from 0.5 to 0.7?

**Answer:** Its predicted class changes from positive to negative without changing the fitted probability

The threshold converts a score into a decision; it need not be fixed at 0.5. Source: section 3.2.1.

### 8. Likelihood of a negative label

A logistic model outputs positive-class probability 0.8. If the observed label is 0, what probability does the model assign to that label?

**Answer:** 0.2

For label 0, the likelihood contribution is 1-p, here 0.2. Source: section 3.2.2.

### 9. Log-likelihood

Why maximize log-likelihood instead of multiplying many small likelihood terms directly?

**Answer:** The logarithm preserves the maximizer and converts products into numerically easier sums

The natural logarithm is strictly increasing. Summing log terms avoids numerical underflow from tiny products. Source: section 3.2.2.

### 10. Tree leaf probability

A decision-tree leaf contains 8 examples, of which 6 have binary label 1. What positive-class probability does the chapter's leaf model return?

**Answer:** 0.75

The leaf prediction is the average binary label: 6/8. Source: section 3.3.2.

### 11. Entropy comparison

Which binary leaf has the greatest label entropy?

**Answer:** A leaf with 5 positive and 5 negative examples

Entropy is maximal at equal class proportions. With natural logarithms the maximum is ln(2), not 1; with base-2 logs it is 1 bit. Source: section 3.3.2.

### 12. Weighted split entropy

A split puts 3 examples in a child with entropy 0.2 and 7 examples in a child with entropy 0.6. What is the weighted child entropy?

**Answer:** 0.48

Use child sample fractions: 0.3*0.2 + 0.7*0.6 = 0.48. Source: section 3.3.2.

### 13. Greedy splitting

Why does the described ID3 procedure not guarantee a globally optimal tree?

**Answer:** It chooses the best available split locally without evaluating all future tree structures

A locally best split need not belong to the globally best full tree. Source: section 3.3.2.

### 14. Tree stopping and pruning

Select TWO statements consistent with the chapter's tree discussion.

**Answer:** Pruning removes branches whose benefit does not justify retaining them; A maximum depth can stop recursive splitting

Depth and minimum improvement are controls on growth; pruning can reduce overfitting. Source: section 3.3.2.

### 15. Hinge loss inside margin

For positive label y = +1 and score s = w dot x - b = 0.4, what is hinge loss max(0, 1-y*s)?

**Answer:** 0.6

The sign is correct, but the example is inside the unit score margin: 1-0.4=0.6. Source: section 3.4.1.

### 16. Hinge loss outside margin

For label y = -1 and score s = -2, what is hinge loss max(0, 1-y*s)?

**Answer:** 0

The signed score y*s is 2, so max(0, 1-2)=0. Source: section 3.4.1.

### 17. Book-specific C convention

Use the BOOK'S objective: C*||w||^2 + mean hinge loss. What does increasing C directly emphasize?

**Answer:** The norm penalty, relative to the training hinge-loss term

Here C multiplies the norm penalty. Many libraries instead put C on the loss term, giving the opposite direction; always inspect the objective. Source: section 3.4.1.

### 18. Kernel trick

What does the kernel trick let SVM compute without explicitly materializing transformed feature vectors?

**Answer:** Their dot products in an implicit feature space

A kernel provides k(x,z)=phi(x) dot phi(z); optimization can use these similarities directly. Source: section 3.4.2.

### 19. Quadratic kernel

For x = [1,2] and z = [3,4], compute the quadratic kernel k(x,z) = (x dot z)^2.

**Answer:** 121

The dot product is 1*3+2*4=11; squaring gives 121. Source: section 3.4.2.

### 20. RBF similarity

For a fixed positive sigma, how does the RBF kernel change as the Euclidean distance between two inputs increases?

**Answer:** It decreases toward zero

The RBF is exp(-distance^2/(2*sigma^2)); it equals one at zero distance and decreases with distance. Source: section 3.4.2.

### 21. kNN predictions

Match each kNN situation to its prediction or property.

**Answer:** Classification neighbor labels A, A, B → Predict class A by majority; Regression neighbor targets 2, 4, 9 → Predict 5 by arithmetic mean; Changing the chosen k → Changing a hyperparameter; Making a query after training → Consult stored labeled examples

Ordinary kNN retains examples and aggregates labels from a selected neighborhood. Source: section 3.5.

### 22. Euclidean distance

What is the Euclidean distance between [1,2] and [4,6]?

**Answer:** 5

The distance is sqrt(3^2+4^2)=5. Source: section 3.5.

### 23. Orthogonal cosine

What is the cosine similarity of the nonzero vectors [1,0] and [0,2]?

**Answer:** 0

The dot product is zero, so their cosine similarity is zero. Source: section 3.5.

### 24. Choose a model under constraints

You need many very fast predictions with limited serving memory. Compare a fitted linear model and ordinary kNN; mention one reason you might still prefer kNN.

**Answer:** Use the rubric below.

Self-assessment: mark correct only if your answer includes ALL of the following. A fitted linear model stores a coefficient vector and predicts with a dot product; ordinary kNN retains training examples and performs neighbor search; kNN may better fit a nonlinear local pattern or need little fitting, so accuracy and the data geometry may justify its prediction cost. Exact performance depends on indexing and implementation. Source: section 3.1 and 3.5.

## Chapter 4 — Anatomy of a Learning Algorithm

### 1. Algorithm building blocks

Match each linear-regression component to its role.

**Answer:** Squared residual for one example → Loss function; Mean squared residual over training data → Optimization criterion; Gradient descent → Optimization routine; w dot x + b → Prediction model

The chapter separates a per-example loss, an aggregate criterion, and a procedure for optimizing it. Source: section 4.1.

### 2. Descent direction

Which update is gradient descent for a parameter theta and positive learning rate alpha?

**Answer:** theta <- theta - alpha * gradient of the objective

The gradient points toward steepest local increase; descent takes the opposite direction. Source: section 4.1–4.2.

### 3. One scalar update

A parameter is 3, its current derivative is 4, and the learning rate is 0.1. What is its value after one gradient-descent step?

**Answer:** 2.6

3 - 0.1*4 = 2.6. Source: section 4.2.

### 4. Negative derivative update

A parameter is 3, its current derivative is -4, and the learning rate is 0.1. What is its next value?

**Answer:** 3.4

Subtracting a negative derivative increases the parameter: 3 - 0.1*(-4) = 3.4. Source: section 4.2.

### 5. MSE derivative w

There is one training pair x=2, y=5. At w=1 and b=1, use MSE = (y-(w*x+b))^2. What is the derivative with respect to w?

**Answer:** -8

The residual y-(w*x+b) is 2. The derivative is -2*x*residual = -8. Source: section 4.2.

### 6. MSE derivative b

For the same single example x=2, y=5, at w=1 and b=1, what is the MSE derivative with respect to b?

**Answer:** -4

The derivative is -2*(y-(w*x+b)) = -4. Source: section 4.2.

### 7. Simultaneous updates

When computing one full-batch step for w and b, which implementation matches the chapter?

**Answer:** Compute both gradients using the old w and b, then update both parameters

Both partial derivatives should be evaluated at the same current parameter vector. Other update schemes are different algorithms. Source: section 4.2.

### 8. Epoch

In the full-batch example, what does an epoch mean?

**Answer:** One complete use of the training set to compute a parameter update

For minibatch training, one epoch still traverses the dataset, but it usually contains multiple parameter updates. Source: section 4.2.

### 9. Large learning rate

What can happen if the learning rate is too large?

**Answer:** Updates can overshoot, oscillate, or diverge rather than converge

Gradient descent is sensitive to step size; a very small learning rate can instead make progress slow. Source: section 4.2.

### 10. Convexity caveat

Which statement is mathematically correct about a differentiable convex objective?

**Answer:** Any local minimum is global, but the minimizer need not be unique

Convexity rules out nonglobal local minima; uniqueness needs additional conditions such as strict convexity. Source: section 4.1.

### 11. Minibatch SGD

How does minibatch stochastic gradient descent reduce the cost of an individual update?

**Answer:** Estimate the gradient from a subset of training examples

A minibatch gradient is cheaper but noisier than a full-batch gradient; overall convergence cost depends on the problem. Source: section 4.2.

### 12. Optimization variants

Match each method to the description emphasized in the chapter.

**Answer:** Minibatch SGD → Uses subsets to estimate a gradient; Adagrad → Adapts per-parameter learning rates using accumulated squared gradients; Momentum → Carries update history to accelerate progress and reduce oscillation

These are optimization procedures, not stand-alone statistical prediction models. Source: section 4.2.

### 13. Solver versus learner

Why is gradient descent not itself a complete machine-learning algorithm?

**Answer:** It is a general optimizer and does not by itself specify the prediction model, loss, and training task

The same optimizer can be used for many different models and objectives, including non-ML problems. Source: section 4.2.

### 14. Library workflow

What is the practical engineering workflow recommended in the chapter?

**Answer:** Use a well-tested library and check its input, output, and hyperparameter documentation

Libraries provide stable implementations, but estimator capabilities and data-shape requirements still matter. Source: section 4.3–4.4.

### 15. Estimator capabilities

Select TWO capabilities to verify before selecting a learning algorithm or implementation.

**Answer:** Whether it supports incremental updates from new labeled batches; Whether it accepts the input feature representation

Feature support, probability output, class weighting, incremental fitting, and target type vary by estimator. Source: section 4.4.

### 16. Class weights

What is the intended effect of assigning a larger training weight to a minority class?

**Answer:** Make errors on that class more costly during fitting, potentially trading errors elsewhere

Weighting changes the optimization tradeoff; it does not guarantee a particular generalization result. Source: section 4.4.

### 17. Debug a training loop

A training loop shows rising or oscillating loss after parameter updates. Give a minimal debugging plan grounded in this chapter.

**Answer:** Use the rubric below.

Self-assessment: mark correct only if your answer includes ALL of the following. Verify the gradient signs and mean-versus-sum scaling; compute all gradient coordinates at the same current parameters; try a smaller learning rate; track the objective over training. Increasing epochs alone does not fix an unstable update. Source: section 4.2.

### 18. Batch update calculation

For one example x=2, y=5, start at w=1, b=1 and use learning rate 0.1. Compute BOTH parameters after one simultaneous MSE gradient step and the new squared error.

**Answer:** Use the rubric below.

Self-assessment: mark correct only if your answer includes ALL of the following. Initial residual is 2; gradients are -8 for w and -4 for b; simultaneous updates give w=1.8 and b=1.4; the new prediction is 5 and the squared error is 0. Source: section 4.2.
