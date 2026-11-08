"""Build portable Bookclub GIFT tests and Anki TSVs. No third-party dependencies."""
from pathlib import Path
import html
import json
import random
import re

STUDY = Path(__file__).resolve().parent
ROOT = STUDY.parents[1]
BOOK_ID = 'hundred-page-machine-learning'
BOOK = 'The Hundred-Page Machine Learning Book'
CHAPTERS = []


def chapter(number, title):
    ch = dict(number=number, title=title, questions=[], cards=[])
    CHAPTERS.append(ch)
    return ch


def single(ch, title, prompt, correct, wrong, explanation, section):
    options = [correct] + wrong
    random.Random(f'{ch["number"]}:{title}').shuffle(options)
    ch['questions'].append(dict(type='single', title=title, prompt=prompt,
        options=options, correct=options.index(correct), explanation=explanation, section=section))


def number(ch, title, prompt, value, explanation, section, tolerance=0):
    ch['questions'].append(dict(type='numerical', title=title, prompt=prompt,
        value=value, tolerance=tolerance, explanation=explanation, section=section))


def multiple(ch, title, prompt, correct, wrong, explanation, section):
    assert len(correct) == 2 and len(wrong) == 2
    options = correct + wrong
    random.Random(f'{ch["number"]}:{title}').shuffle(options)
    ch['questions'].append(dict(type='multiple', title=title, prompt=prompt,
        options=options, correct=[i for i, s in enumerate(options) if s in correct],
        explanation=explanation, section=section))


def matching(ch, title, prompt, pairs, explanation, section):
    ch['questions'].append(dict(type='matching', title=title, prompt=prompt,
        pairs=pairs, explanation=explanation, section=section))


def essay(ch, title, prompt, rubric, section):
    ch['questions'].append(dict(type='essay', title=title, prompt=prompt,
        explanation='Self-assessment: mark correct only if your answer includes ALL of the following. ' + rubric,
        section=section))


def cards(ch, section, items):
    for front, back in items:
        ch['cards'].append(dict(front=front, back=back, section=section))


c = chapter(1, 'Introduction')
single(c, 'Learning from examples', 'Which activity best matches the chapter\'s definition of machine learning?',
       'Building a statistical model from examples to solve a practical problem',
       ['Writing every decision rule by hand without using examples', 'Storing files without deriving a predictive or descriptive model', 'Using a computer for any arithmetic operation'],
       'Machine learning uses a dataset to algorithmically build a statistical model for a practical task.', '1.1')
matching(c, 'Learning settings', 'Match each dataset or interaction setting to its learning type.',
         [('Emails with spam labels', 'Supervised'), ('Unlabeled customer vectors to group', 'Unsupervised'),
          ('A few labeled images plus many unlabeled images', 'Semi-supervised'), ('An agent taking actions and receiving rewards', 'Reinforcement')],
         'The distinctions concern available supervision and, in reinforcement learning, sequential interaction and reward.', '1.2')
single(c, 'Consistent features', 'In a dataset of people, feature position 2 contains weight in kilograms. What must be true of position 2 in other examples?',
       'It must represent the same kind of information with the same meaning and units',
       ['It must contain the same numerical weight for every person', 'It may instead contain age if the model can infer the meaning', 'Its meaning should depend on the target label'],
       'A coordinate must have consistent semantics across examples; its value can differ.', '1.2.1')
single(c, 'Unsupervised output', 'Which task is an example of dimensionality reduction?',
       'Mapping each input vector to a vector with fewer features',
       ['Predicting a provided spam label', 'Selecting an action to maximize future reward', 'Adding a target label as an extra feature'],
       'Dimensionality reduction transforms the representation without requiring target labels.', '1.2.2')
single(c, 'Why unlabeled data helps', 'Why might adding unlabeled examples improve a semi-supervised model?',
       'They can reveal structure in the input distribution that helps learn from the labeled examples',
       ['Every unlabeled example automatically supplies a correct target', 'They remove all need for labeled examples in every problem', 'They guarantee that no future input will be misclassified'],
       'Additional input-distribution information can help, but improvement is not guaranteed.', '1.2.3')
single(c, 'Policy', 'What does a reinforcement-learning policy map, in the chapter\'s description?',
       'A state representation to an action',
       ['An action to a training-set row number', 'A label to a feature-vector dimension', 'A test score to an unconditional reward'],
       'A policy chooses actions based on state, aiming at a long-term reward objective rather than merely an immediate payoff.', '1.2.4')
number(c, 'Bag of words dimension', 'A binary bag-of-words dictionary contains 20,000 words. A dataset contains 10,000 emails. How many features does EACH email vector have?',
       20000, 'Dimensionality is the dictionary size; the number of examples is a separate quantity.', '1.3')
number(c, 'Binary word presence', 'In the chapter\'s binary bag-of-words representation, an email contains the dictionary word "offer" five times. What is that word\'s feature value?',
       1, 'This particular representation records presence, not frequency or word order.', '1.3')
single(c, 'Training versus prediction', 'Which sequence describes prediction with an already trained spam SVM?',
       'Apply the training-time feature encoding, compute the learned linear score, and take its sign',
       ['Relabel all training examples before every prediction', 'Choose a new dictionary ordering independently for each email', 'Optimize the model parameters using the unknown true label of the new email'],
       'Training finds the parameters. Prediction applies the fixed model to a consistently encoded new input.', '1.3')
number(c, 'SVM sign calculation', 'Use the chapter\'s convention: score is w dot x minus b. With w = [2, -1], x = [3, 1], and b = 2, what label (+1 or -1) is predicted?',
       1, 'The score is 2*3 - 1*1 - 2 = 3, so its sign is +1. A score exactly zero would require a tie convention.', '1.3')
number(c, 'Hyperplane dimension', 'In a 12-dimensional input space, how many dimensions does a nondegenerate linear decision hyperplane have?',
       11, 'One independent linear equality reduces the dimension by one.', '1.3')
single(c, 'Hard-margin constraint', 'Which is the compact hard-margin SVM constraint for every training example in the chapter\'s notation?',
       'y_i * (w dot x_i - b) >= 1',
       ['y_i * (w dot x_i - b) <= 0', 'w dot x_i - b = 0 for all examples', 'The norm of w must equal the number of examples'],
       'For labels +1 and -1, this enforces both correct classification and a score margin of at least one.', '1.3')
number(c, 'Margin width', 'For the canonical hard-margin constraints, the distance between the two supporting hyperplanes is 2 / ||w||. If ||w|| is 4, what is the full margin width?',
       0.5, 'The width is 2/4 = 0.5. Minimizing the norm increases this margin subject to the constraints.', '1.3')
multiple(c, 'Beyond accuracy', 'Select TWO practical considerations the chapter gives in addition to predictive accuracy.',
         ['Model-building time', 'Prediction-processing time'], ['Whether the filename is alphabetically first', 'Whether all training labels are identical'],
         'Training cost and inference latency can justify choosing a somewhat less accurate model.', '1.3')
single(c, 'Generalization assumptions', 'Which situation most directly supports the chapter\'s intuition about performance on new data?',
       'Training and future examples are independently sampled using the same data-generating procedure',
       ['Future inputs intentionally come from a completely different population', 'Every training example is a duplicate of one atypical observation', 'The model is evaluated only on data it memorized'],
       'Comparable, representative sampling supports generalization; it is not an unconditional guarantee.', '1.4')
single(c, 'Perfect separation is not always possible', 'Why might no hyperplane perfectly separate the training classes?',
       'Noise, label errors, outliers, or genuinely nonlinear class structure',
       ['The presence of more than one input feature always prevents separation', 'SVM never uses numerical features', 'Every binary dataset is linearly separable by definition'],
       'The chapter introduces limits of the simple hard-margin linear setup, developed further in Chapter 3.', '1.3')
essay(c, 'Sampling shift diagnosis', 'A spam model is trained on personal English emails, then deployed on corporate messages in another language. Explain why high training accuracy may not transfer.',
      'The training and deployment distributions differ; the learned features or boundary may not describe the new population; training accuracy alone does not establish performance on that population.', '1.4')
essay(c, 'Learning pipeline', 'Describe an end-to-end supervised spam-detection pipeline, distinguishing training from prediction.',
      'Collect input-label pairs; choose a consistent feature encoding; train to learn model parameters; encode unseen emails the same way and apply the learned model without using their unknown labels.', '1.3')
cards(c, '1.1', [
    ('What is machine learning in this book\'s practical definition?', 'Gathering examples and algorithmically building a statistical model to solve a practical problem.'),
])
cards(c, '1.2.1', [
    ('What information does a supervised-learning dataset contain?', 'Pairs (x_i, y_i): an input feature vector and its target label.'),
    ('What is a feature vector?', 'An ordered collection of values describing an example; each coordinate has a consistent meaning across examples.'),
    ('What is the goal of supervised learning?', 'Learn a model that maps an input to a label, or to information from which a label can be deduced.'),
])
cards(c, '1.2.2', [
    ('What distinguishes unsupervised learning from supervised learning?', 'Its training examples do not include target labels; the algorithm learns useful structure or representations.'),
    ('What does a clustering model assign to an example?', 'A cluster identifier indicating a group of related examples.'),
    ('What is the output of dimensionality reduction?', 'A representation with fewer features than the original input vector.'),
    ('What does an outlier-detection score describe?', 'How atypical an example is relative to the data; the score\'s numerical direction depends on the implementation.'),
])
cards(c, '1.2.3', [
    ('What data does semi-supervised learning use?', 'Both labeled and unlabeled examples, often with many more unlabeled examples.'),
    ('Why can unlabeled data help semi-supervised learning?', 'It reveals the input distribution or structure, which may improve learning from limited labels; this is not guaranteed.'),
])
cards(c, '1.2.4', [
    ('What does a reinforcement-learning policy map?', 'A representation of the environment\'s state to an action, aiming to optimize a long-term reward objective.'),
    ('What distinguishes reinforcement learning from one-shot supervised prediction?', 'Actions can affect later states and rewards, so decisions are sequential and consequences extend into the future.'),
])
cards(c, '1.3', [
    ('What does one feature record in the chapter\'s binary bag-of-words example?', 'Whether a particular dictionary word occurs: 1 if present, 0 otherwise; repeated occurrences do not increase the value.'),
    ('In bag-of-words encoding, what determines input dimensionality?', 'The dictionary size, not the number of documents.'),
    ('What is a decision boundary?', 'The boundary between regions of input space assigned different predicted classes.'),
    ('What is the chapter\'s linear SVM prediction rule?', 'Predict sign(w* dot x - b*), where the starred parameters were learned during training. A zero score needs a tie convention.'),
    ('What is the canonical hard-margin SVM constraint?', 'For every example with y_i in {-1, +1}: y_i (w dot x_i - b) >= 1.'),
    ('How does canonical SVM margin width depend on ||w||?', 'The full width is 2/||w||. Subject to the canonical constraints, a smaller norm gives a larger margin.'),
    ('Besides accuracy, which two runtime costs matter when choosing an algorithm?', 'The time to build/train the model and the time to process predictions.'),
])
cards(c, '1.4', [
    ('What sampling assumption supports the chapter\'s generalization intuition?', 'Training and future examples should come from the same data-generating process, with independent and representative sampling. Distribution shift can break this intuition.'),
])

c = chapter(2, 'Notation and Definitions')
matching(c, 'Data structures', 'Match each mathematical object to its description.',
         [('Scalar', 'One numerical value'), ('Vector', 'An ordered list of numerical values'), ('Matrix', 'A rectangular array of numerical values'), ('Set', 'An unordered collection of unique elements')],
         'Ordering matters for vectors, but not for sets; repeated elements do not increase set cardinality.', '2.1.1')
single(c, 'Indexed feature notation', 'What does x_i^(j) denote in the book?',
       'Feature j of example i', ['Example j raised to the power i', 'The j-th power of the whole dataset', 'The number of examples multiplied by the number of features'],
       'The parenthesized superscript is an index, not an exponent.', '2.1.1')
number(c, 'Sigma', 'Compute the sum of 2i for i from 1 through 4.', 20,
       '2 + 4 + 6 + 8 = 20.', '2.1.2')
number(c, 'Pi', 'Compute the product of i for i from 1 through 4.', 24,
       '1 * 2 * 3 * 4 = 24.', '2.1.3')
single(c, 'Set operations', 'Let A contain 1, 3, 5 and B contain 3, 4. Which is their intersection?',
       'The set containing only 3', ['The set containing 1, 3, 4, 5', 'The ordered list 1, 3, 5, 3, 4', 'The empty set'],
       'Intersection retains elements present in both sets; union would contain 1, 3, 4, 5.', '2.1.4')
number(c, 'Derived set', 'Let S contain 1, 3, 4, 5. Form T from x squared for x in S with x > 3. What is the sum of the elements of T?',
       41, 'Only 4 and 5 satisfy the condition; T contains 16 and 25, whose sum is 41.', '2.1.4')
number(c, 'Dot product', 'Compute the dot product of [2, -1, 3] and [4, 5, 0].', 3,
       '2*4 + (-1)*5 + 3*0 = 3. A dot product is a scalar.', '2.1.5')
single(c, 'Matrix-vector shape', 'W has 3 rows and 2 columns. x is a column vector with 2 entries. What is the shape of Wx?',
       'A column vector with 3 entries', ['A column vector with 2 entries', 'A 2-by-3 matrix', 'The product is undefined'],
       'The inner dimensions match, and each row of W produces one output entry.', '2.1.5')
single(c, 'Arg max', 'For inputs a, b, c, a function returns 2, 7, 4 respectively. What does arg max return?',
       'b', ['7', 'c', 'The sum 13'],
       'arg max returns a maximizing input; max returns the output value 7.', '2.1.7')
single(c, 'Local versus global', 'Which statement about a local minimum is correct?',
       'It is no higher than nearby values, but a lower value may exist elsewhere',
       ['It must be the unique global minimum', 'It must have a strictly positive derivative', 'It is always higher than every neighboring value'],
       'Local optimality concerns a neighborhood, while global optimality concerns the full domain.', '2.1.6')
number(c, 'Chain rule', 'For F(x) = (3x + 1)^2, what is F\'(2)?', 42,
       'F\'(x) = 2(3x+1)*3, so F\'(2) = 42.', '2.1.9')
single(c, 'Gradient', 'For f(u,v) = 3u + 2v + 7, what is the gradient with coordinates ordered u, v?',
       '[3, 2]', ['[u, v]', '[3u, 2v]', '7'],
       'Take one partial derivative per coordinate, holding the other coordinate constant.', '2.1.9')
single(c, 'Density versus probability', 'A random variable has a continuous density. Which statement is correct?',
       'An interval probability is an area under the density; a single point has probability zero',
       ['The density height at x is always the probability of exactly x', 'A density must be at most one at every point', 'All continuous distributions assign positive probability to every individual point'],
       'A density is not a probability mass function. Its integral is one; its height can exceed one.', '2.2')
number(c, 'Expectation', 'X takes value 0 with probability 0.25 and value 4 with probability 0.75. What is E[X]?',
       3, 'The probability-weighted average is 0*0.25 + 4*0.75 = 3.', '2.2')
number(c, 'Variance', 'X takes 0 and 2, each with probability 0.5. What is its variance?',
       1, 'Its mean is 1, so variance is 0.5*(0-1)^2 + 0.5*(2-1)^2 = 1.', '2.2')
single(c, 'Unbiased does not mean exact', 'What does it mean for an estimator of a quantity to be unbiased?',
       'Its expectation over repeated samples equals the true quantity',
       ['Its value equals the true quantity for every possible sample', 'It has zero variance', 'It never uses random samples'],
       'An individual estimate can be wrong even when the estimator is unbiased.', '2.3')
number(c, 'Sample mean', 'For the observed sample 2, 4, 9, what is the sample mean?',
       5, '(2+4+9)/3 = 5; the sample mean is an unbiased estimator of the population mean under the usual sampling assumptions.', '2.3')
number(c, 'Bayes calculation', 'P(A) = 0.2, P(B given A) = 0.6, and P(B) = 0.3. What is P(A given B)?',
       0.4, 'Bayes\' rule gives 0.6*0.2/0.3 = 0.4.', '2.4')
matching(c, 'Bayesian terms', 'Match each Bayesian term to its meaning.',
         [('Prior', 'Belief about parameters before the current data'), ('Likelihood', 'Data probability or density as a function of parameters'),
          ('Posterior', 'Belief about parameters after conditioning on data'), ('MAP estimate', 'Parameter value maximizing the posterior')],
         'Posterior is proportional to likelihood times prior; evidence normalizes it.', '2.5')
multiple(c, 'Parameters and hyperparameters', 'Select TWO hyperparameters rather than fitted model coefficients.',
         ['The chosen k in k-nearest neighbors', 'The chosen maximum depth of a decision tree'],
         ['A fitted linear-regression coefficient', 'A fitted linear-regression intercept'],
         'Hyperparameters control the learning setup; coefficients and intercept are fitted within that setup. Hyperparameters can themselves be selected using validation.', '2.6')
matching(c, 'Prediction targets', 'Match each target type to the appropriate task.',
         [('Spam or not spam', 'Binary classification'), ('One of cat, dog, horse', 'Multiclass classification'),
          ('A house price in euros', 'Regression'), ('One of three numeric class codes', 'Multiclass classification, despite numeric encoding')],
         'Task type depends on target meaning, not whether its storage format is numeric.', '2.7')
single(c, 'Instance-based learning', 'Why does ordinary kNN need the training examples when predicting?',
       'Its predictions depend on finding nearby stored examples and their labels',
       ['It fits a fixed coefficient vector and discards all examples', 'It cannot use a distance function', 'It requires the true target of the query before searching'],
       'The stored examples are central to its instance-based prediction procedure.', '2.8')
single(c, 'Deep representation', 'What distinguishes the deep-learning description in this chapter?',
       'Multiple learned layers, with later layers receiving representations produced by preceding layers',
       ['Any dataset with more than two rows', 'Any model trained for a large number of epochs', 'Using a vector rather than a scalar input'],
       'Depth concerns successive learned transformations, not merely dataset size or training duration.', '2.9')
essay(c, 'Bayesian sequential update', 'Explain how to update beliefs about a fixed parameter after two conditionally independent observations.',
      'Start with a prior; multiply by the first observation\'s likelihood and normalize; use that posterior as the next prior; multiply by the second likelihood and normalize. Equivalently the final posterior is proportional to the original prior times both likelihoods. Do not count the prior twice.', '2.5')
cards(c, '2.1.1', [
    ('What is the difference between a vector and a set?', 'A vector is ordered and may repeat values; a set is unordered and contains unique elements.'),
    ('What does x_i^(j) mean in the book\'s notation?', 'Coordinate j of example i; the parenthesized superscript is an index, not a power.'),
    ('What is a matrix?', 'A rectangular array of numbers organized into rows and columns.'),
    ('How do the intervals [a,b] and (a,b) differ?', '[a,b] includes both endpoints; (a,b) excludes both endpoints.'),
])
cards(c, '2.1.2–2.1.4', [
    ('What do capital sigma and capital pi denote?', 'Sigma denotes summation; capital pi denotes multiplication over indexed terms.'),
    ('What does the cardinality |S| of a finite set mean?', 'The number of unique elements in S.'),
    ('How do set intersection and union differ?', 'Intersection contains elements belonging to both sets; union contains elements belonging to either set.'),
])
cards(c, '2.1.5', [
    ('How is the dot product of equal-length vectors computed, and what does it return?', 'Multiply corresponding coordinates and sum: w dot x = sum_j w_j*x_j. The result is a scalar.'),
    ('If W is m-by-n and x is an n-entry column vector, what shape is Wx?', 'An m-entry column vector; each output is the dot product of one row of W with x.'),
    ('What does transposing a column vector do?', 'It makes a row vector with the same entries.'),
])
cards(c, '2.1.6–2.1.8', [
    ('How does a local minimum differ from a global minimum?', 'A local minimum is no higher than nearby values; a global minimum is no higher than any value in the entire domain.'),
    ('What is the difference between max f(x) and arg max f(x)?', 'max returns the largest output value; arg max returns an input attaining it. There can be multiple maximizing inputs.'),
    ('What does the assignment arrow mean?', 'Replace the variable on the left with the value of the expression on the right.'),
])
cards(c, '2.1.9', [
    ('What does a positive or negative derivative indicate locally?', 'A positive derivative indicates local increase as the input increases; a negative derivative indicates local decrease.'),
    ('What is the chain rule for F(x) = f(g(x))?', 'F\'(x) = f\'(g(x))*g\'(x): differentiate the outer function and multiply by the inner derivative.'),
    ('What is a gradient?', 'The vector of partial derivatives, one per input coordinate; each partial derivative holds the other coordinates fixed.'),
    ('Does a zero derivative by itself prove a minimum?', 'No. It may indicate a maximum, a minimum, or another stationary point. Additional reasoning is needed.'),
])
cards(c, '2.2', [
    ('What conditions must a probability mass function satisfy?', 'Every probability is nonnegative, and the probabilities over all possible discrete outcomes sum to one.'),
    ('How do you obtain an interval probability from a continuous density?', 'Integrate the density over the interval. A single point has zero probability for a distribution with a density.'),
    ('Must a probability density be at most one?', 'No. Its height may exceed one; it must be nonnegative and its total integral must equal one.'),
    ('What is the expectation of a discrete random variable?', 'E[X] = sum_x x*P(X=x), when the expectation exists.'),
    ('How are variance and standard deviation defined?', 'Variance is E[(X - E[X])^2]. Standard deviation is its square root.'),
])
cards(c, '2.3', [
    ('What makes an estimator unbiased?', 'Its expectation over repeated samples equals the quantity being estimated. Individual estimates need not be exact.'),
    ('What is the sample mean?', 'The sum of the N observed values divided by N; it is an unbiased estimator of the population mean under the usual sampling assumptions.'),
])
cards(c, '2.4–2.5', [
    ('State Bayes\' rule for events A and B with P(B) > 0.', 'P(A given B) = P(B given A)*P(A)/P(B).'),
    ('How are Bayesian posterior, likelihood, and prior related?', 'Posterior is proportional to likelihood times prior; normalize by the evidence.'),
    ('What does maximum a posteriori (MAP) estimation select?', 'A parameter value maximizing the posterior given the full observed data. Unlike maximum likelihood, MAP includes the prior.'),
])
cards(c, '2.6–2.9', [
    ('How do model parameters differ from hyperparameters?', 'Model parameters are fitted during training; hyperparameters control the model or training setup and may be chosen using validation.'),
    ('How do classification and regression targets differ?', 'Classification predicts a member of a finite set of classes; regression predicts a real-valued target. Numeric class codes remain classification.'),
    ('How does instance-based kNN differ from a fixed-parameter fitted model?', 'kNN retains examples and consults neighbors at prediction time; many fitted parametric models can predict without retaining their training examples.'),
    ('What distinguishes deep learning from shallow learning in the chapter?', 'Deep models learn a succession of representations through multiple layers; later layers use outputs of preceding learned layers rather than only the original features.'),
])

c = chapter(3, 'Fundamental Algorithms')
number(c, 'Linear prediction', 'For f(x) = w dot x + b, w = [2, -1], x = [3, 4], b = 5, what is f(x)?',
       7, '2*3 - 1*4 + 5 = 7.', '3.1.1')
number(c, 'MSE', 'A model predicts 1 and 5 for targets 3 and 4. What is the mean squared error?',
       2.5, 'The squared errors are 4 and 1; their average is 2.5.', '3.1.2')
single(c, 'Why square errors', 'Which is a useful property of squared-error loss compared with absolute-error loss?',
       'It is differentiable everywhere and increasingly penalizes larger residual magnitudes',
       ['It never responds to outliers', 'It makes every regression objective nonconvex', 'It guarantees that any fitted model generalizes perfectly'],
       'Squaring is smooth and magnifies large errors. That also makes it sensitive to large residuals.', '3.1.2')
single(c, 'Overfitting', 'Which outcome is characteristic of overfitting?',
       'Very low training error but substantially worse error on representative unseen examples',
       ['Identical low errors on training and unseen examples', 'A model with no fitted parameters by definition', 'An optimizer that always stops before reading the data'],
       'Fitting training peculiarities does not necessarily capture patterns that persist in new data.', '3.1.2')
single(c, 'Logistic task', 'Despite its name, what task does binary logistic regression solve?',
       'Classification', ['Only continuous-target regression', 'Only clustering', 'Only dimensionality reduction'],
       'Its sigmoid output can be interpreted as a positive-class probability and thresholded into a class.', '3.2')
number(c, 'Sigmoid at zero', 'What is sigmoid(0), where sigmoid(z) = 1/(1+exp(-z))?',
       0.5, 'exp(0)=1, so the result is 1/2.', '3.2.1')
single(c, 'Threshold is a choice', 'A logistic model assigns positive-class probability 0.6. What happens if the threshold is raised from 0.5 to 0.7?',
       'Its predicted class changes from positive to negative without changing the fitted probability',
       ['Its fitted coefficients must automatically be retrained', 'The probability becomes 0.7', 'It must still predict positive because thresholds never matter'],
       'The threshold converts a score into a decision; it need not be fixed at 0.5.', '3.2.1')
number(c, 'Likelihood of a negative label', 'A logistic model outputs positive-class probability 0.8. If the observed label is 0, what probability does the model assign to that label?',
       0.2, 'For label 0, the likelihood contribution is 1-p, here 0.2.', '3.2.2', 0.000000001)
single(c, 'Log-likelihood', 'Why maximize log-likelihood instead of multiplying many small likelihood terms directly?',
       'The logarithm preserves the maximizer and converts products into numerically easier sums',
       ['The logarithm reverses the order of all positive likelihoods', 'Log-likelihood ignores all negative labels', 'This always yields a closed-form logistic-regression solution'],
       'The natural logarithm is strictly increasing. Summing log terms avoids numerical underflow from tiny products.', '3.2.2')
number(c, 'Tree leaf probability', 'A decision-tree leaf contains 8 examples, of which 6 have binary label 1. What positive-class probability does the chapter\'s leaf model return?',
       0.75, 'The leaf prediction is the average binary label: 6/8.', '3.3.2')
single(c, 'Entropy comparison', 'Which binary leaf has the greatest label entropy?',
       'A leaf with 5 positive and 5 negative examples',
       ['A leaf with 10 positive and no negative examples', 'A leaf with no positive and 10 negative examples', 'A leaf with 9 positive and 1 negative example'],
       'Entropy is maximal at equal class proportions. With natural logarithms the maximum is ln(2), not 1; with base-2 logs it is 1 bit.', '3.3.2')
number(c, 'Weighted split entropy', 'A split puts 3 examples in a child with entropy 0.2 and 7 examples in a child with entropy 0.6. What is the weighted child entropy?',
       0.48, 'Use child sample fractions: 0.3*0.2 + 0.7*0.6 = 0.48.', '3.3.2', 0.000000001)
single(c, 'Greedy splitting', 'Why does the described ID3 procedure not guarantee a globally optimal tree?',
       'It chooses the best available split locally without evaluating all future tree structures',
       ['It never consults the example labels', 'It explicitly evaluates every possible complete tree', 'Entropy cannot be calculated for binary data'],
       'A locally best split need not belong to the globally best full tree.', '3.3.2')
multiple(c, 'Tree stopping and pruning', 'Select TWO statements consistent with the chapter\'s tree discussion.',
         ['A maximum depth can stop recursive splitting', 'Pruning removes branches whose benefit does not justify retaining them'],
         ['Every leaf must always contain exactly one example', 'A larger tree is guaranteed to generalize better'],
         'Depth and minimum improvement are controls on growth; pruning can reduce overfitting.', '3.3.2')
number(c, 'Hinge loss inside margin', 'For positive label y = +1 and score s = w dot x - b = 0.4, what is hinge loss max(0, 1-y*s)?',
       0.6, 'The sign is correct, but the example is inside the unit score margin: 1-0.4=0.6.', '3.4.1', 0.000000001)
number(c, 'Hinge loss outside margin', 'For label y = -1 and score s = -2, what is hinge loss max(0, 1-y*s)?',
       0, 'The signed score y*s is 2, so max(0, 1-2)=0.', '3.4.1')
single(c, 'Book-specific C convention', 'Use the BOOK\'S objective: C*||w||^2 + mean hinge loss. What does increasing C directly emphasize?',
       'The norm penalty, relative to the training hinge-loss term',
       ['The hinge-loss term, relative to the norm penalty', 'The number of input features', 'The number of neighbors in kNN'],
       'Here C multiplies the norm penalty. Many libraries instead put C on the loss term, giving the opposite direction; always inspect the objective.', '3.4.1')
single(c, 'Kernel trick', 'What does the kernel trick let SVM compute without explicitly materializing transformed feature vectors?',
       'Their dot products in an implicit feature space',
       ['The exact true label of every future example', 'All possible trees in constant time', 'A guarantee of separability for every dataset and kernel'],
       'A kernel provides k(x,z)=phi(x) dot phi(z); optimization can use these similarities directly.', '3.4.2')
number(c, 'Quadratic kernel', 'For x = [1,2] and z = [3,4], compute the quadratic kernel k(x,z) = (x dot z)^2.',
       121, 'The dot product is 1*3+2*4=11; squaring gives 121.', '3.4.2')
single(c, 'RBF similarity', 'For a fixed positive sigma, how does the RBF kernel change as the Euclidean distance between two inputs increases?',
       'It decreases toward zero', ['It increases without bound', 'It stays exactly one', 'It becomes a negative probability'],
       'The RBF is exp(-distance^2/(2*sigma^2)); it equals one at zero distance and decreases with distance.', '3.4.2')
matching(c, 'kNN predictions', 'Match each kNN situation to its prediction or property.',
         [('Classification neighbor labels A, A, B', 'Predict class A by majority'), ('Regression neighbor targets 2, 4, 9', 'Predict 5 by arithmetic mean'),
          ('Changing the chosen k', 'Changing a hyperparameter'), ('Making a query after training', 'Consult stored labeled examples')],
         'Ordinary kNN retains examples and aggregates labels from a selected neighborhood.', '3.5')
number(c, 'Euclidean distance', 'What is the Euclidean distance between [1,2] and [4,6]?',
       5, 'The distance is sqrt(3^2+4^2)=5.', '3.5')
number(c, 'Orthogonal cosine', 'What is the cosine similarity of the nonzero vectors [1,0] and [0,2]?',
       0, 'The dot product is zero, so their cosine similarity is zero.', '3.5')
essay(c, 'Choose a model under constraints', 'You need many very fast predictions with limited serving memory. Compare a fitted linear model and ordinary kNN; mention one reason you might still prefer kNN.',
      'A fitted linear model stores a coefficient vector and predicts with a dot product; ordinary kNN retains training examples and performs neighbor search; kNN may better fit a nonlinear local pattern or need little fitting, so accuracy and the data geometry may justify its prediction cost. Exact performance depends on indexing and implementation.', '3.1 and 3.5')
cards(c, '3.1', [
    ('What is the linear-regression prediction formula?', 'f(x) = w dot x + b, where w contains fitted feature weights and b is a fitted intercept.'),
    ('What objective does ordinary least-squares regression minimize?', 'Mean squared error: the average of (prediction - target)^2 over the training examples.'),
    ('What is empirical risk?', 'The average loss evaluated on the observed training examples; it estimates expected loss under the data distribution.'),
    ('Why are large residuals especially influential under squared-error loss?', 'Their loss grows quadratically rather than linearly with residual magnitude.'),
    ('What is overfitting?', 'Capturing training-specific patterns so that training performance is much better than performance on representative unseen examples.'),
    ('Does a linear model guarantee absence of overfitting?', 'No. Linear models can overfit, especially with many features, little data, or noisy features. Simplicity is not a guarantee.'),
])
cards(c, '3.2', [
    ('Is logistic regression a classification or regression algorithm in this chapter?', 'Classification, despite its name.'),
    ('What is the standard sigmoid function?', 'sigmoid(z) = 1/(1+exp(-z)); for finite real z its output is strictly between 0 and 1.'),
    ('What is sigmoid(0)?', '0.5.'),
    ('How does a binary logistic model produce a class prediction?', 'Compute p = sigmoid(w dot x + b), then compare p with a chosen decision threshold, often 0.5.'),
    ('What likelihood contribution does one binary example make if the model predicts positive probability p?', 'p if the observed label is 1; 1-p if it is 0. Combined notation: p^y * (1-p)^(1-y).'),
    ('Under conditional independence, how is a dataset likelihood built from example likelihoods?', 'Multiply the contributions of the individual observations.'),
    ('Why does taking the logarithm preserve a positive-likelihood maximizer?', 'The logarithm is strictly increasing, so it preserves the ordering of positive likelihood values.'),
    ('What is binary logistic negative log-likelihood for one example?', '-[y*ln(p) + (1-y)*ln(1-p)]. It penalizes confident wrong predictions strongly.'),
    ('Does ordinary logistic regression have a general closed-form fitting solution?', 'No; it is typically fitted by numerical optimization.'),
])
cards(c, '3.3', [
    ('What does an internal node of the chapter\'s decision tree do?', 'Test a feature against a threshold and route the example to one child.'),
    ('What probability does a binary decision-tree leaf estimate in the chapter?', 'The fraction of training examples in that leaf with label 1.'),
    ('How does binary label entropy behave at pure and balanced leaves?', 'It is zero at a pure leaf and largest at equal class proportions.'),
    ('What is the maximum binary entropy with natural logs versus base-2 logs?', 'ln(2) with natural logs; 1 bit with base-2 logs. The log base changes the scale, not the best split.'),
    ('How is a split\'s child entropy aggregated?', 'Take the sum of each child entropy weighted by that child\'s fraction of the parent examples.'),
    ('Why is greedy decision-tree learning not guaranteed globally optimal?', 'Each split is selected locally without searching every possible future subtree.'),
    ('Name two controls that can stop tree growth.', 'Examples include maximum depth, minimum entropy reduction, a pure leaf, or no useful available split.'),
    ('What is pruning in a decision tree?', 'Removing or replacing branches whose contribution does not justify their complexity, often to improve generalization.'),
])
cards(c, '3.4', [
    ('What is the difference between hard-margin and soft-margin SVM?', 'Hard margin requires all canonical margin constraints; soft margin allows violations and penalizes them in the objective.'),
    ('What is hinge loss for label y in {-1,+1} and linear score s?', 'max(0, 1-y*s). It is zero when the signed score is at least one.'),
    ('Can a correctly classified example have positive hinge loss?', 'Yes. If 0 < y*s < 1, it has the correct sign but lies inside the margin.'),
    ('In the BOOK\'S objective C*||w||^2 + mean hinge loss, what does larger C emphasize?', 'The norm penalty relative to hinge loss. This is opposite to common formulations placing C on the loss term.'),
    ('What does a kernel function compute for an implicit feature mapping phi?', 'k(x,z) = phi(x) dot phi(z), without necessarily constructing the mapped vectors.'),
    ('What is the quadratic kernel used in the chapter?', 'k(x,z) = (x dot z)^2.'),
    ('What is the RBF kernel formula?', 'k(x,z) = exp(-||x-z||^2/(2*sigma^2)), for sigma > 0; it decreases as input distance increases.'),
])
cards(c, '3.5', [
    ('How does ordinary kNN aggregate neighbors for classification versus regression?', 'Classification: majority label. Regression: arithmetic mean of neighbor targets. Ties and weighting require additional choices.'),
    ('Which two kNN choices discussed in the chapter are hyperparameters?', 'The number of neighbors k and the choice of distance or similarity measure.'),
    ('How is Euclidean distance between two vectors computed?', 'Take the square root of the sum of squared coordinate differences: sqrt(sum_j (x_j-z_j)^2).'),
    ('What cosine similarities correspond to same-direction, orthogonal, and opposite-direction nonzero vectors?', 'Same direction: 1. Orthogonal: 0. Opposite direction: -1. Cosine similarity is undefined for a zero vector unless an implementation adopts a special convention.'),
])

c = chapter(4, 'Anatomy of a Learning Algorithm')
matching(c, 'Algorithm building blocks', 'Match each linear-regression component to its role.',
         [('Squared residual for one example', 'Loss function'), ('Mean squared residual over training data', 'Optimization criterion'),
          ('Gradient descent', 'Optimization routine'), ('w dot x + b', 'Prediction model')],
         'The chapter separates a per-example loss, an aggregate criterion, and a procedure for optimizing it.', '4.1')
single(c, 'Descent direction', 'Which update is gradient descent for a parameter theta and positive learning rate alpha?',
       'theta <- theta - alpha * gradient of the objective',
       ['theta <- theta + alpha * gradient of the objective', 'theta <- alpha regardless of the gradient', 'theta <- the true target of the next unseen example'],
       'The gradient points toward steepest local increase; descent takes the opposite direction.', '4.1–4.2')
number(c, 'One scalar update', 'A parameter is 3, its current derivative is 4, and the learning rate is 0.1. What is its value after one gradient-descent step?',
       2.6, '3 - 0.1*4 = 2.6.', '4.2', 0.000000001)
number(c, 'Negative derivative update', 'A parameter is 3, its current derivative is -4, and the learning rate is 0.1. What is its next value?',
       3.4, 'Subtracting a negative derivative increases the parameter: 3 - 0.1*(-4) = 3.4.', '4.2', 0.000000001)
number(c, 'MSE derivative w', 'There is one training pair x=2, y=5. At w=1 and b=1, use MSE = (y-(w*x+b))^2. What is the derivative with respect to w?',
       -8, 'The residual y-(w*x+b) is 2. The derivative is -2*x*residual = -8.', '4.2')
number(c, 'MSE derivative b', 'For the same single example x=2, y=5, at w=1 and b=1, what is the MSE derivative with respect to b?',
       -4, 'The derivative is -2*(y-(w*x+b)) = -4.', '4.2')
single(c, 'Simultaneous updates', 'When computing one full-batch step for w and b, which implementation matches the chapter?',
       'Compute both gradients using the old w and b, then update both parameters',
       ['Update w for each example, but compute b using the final w and call it the same full-batch step', 'Compute the b gradient using an unknown future target', 'Skip the gradient calculation whenever the loss is positive'],
       'Both partial derivatives should be evaluated at the same current parameter vector. Other update schemes are different algorithms.', '4.2')
single(c, 'Epoch', 'In the full-batch example, what does an epoch mean?',
       'One complete use of the training set to compute a parameter update',
       ['One parameter regardless of the number of examples', 'One prediction on an unseen example', 'The number of feature columns'],
       'For minibatch training, one epoch still traverses the dataset, but it usually contains multiple parameter updates.', '4.2')
single(c, 'Large learning rate', 'What can happen if the learning rate is too large?',
       'Updates can overshoot, oscillate, or diverge rather than converge',
       ['The objective is guaranteed to decrease at every step', 'The model automatically loses all hyperparameters', 'All gradients become exactly zero by definition'],
       'Gradient descent is sensitive to step size; a very small learning rate can instead make progress slow.', '4.2')
single(c, 'Convexity caveat', 'Which statement is mathematically correct about a differentiable convex objective?',
       'Any local minimum is global, but the minimizer need not be unique',
       ['It necessarily has exactly one minimizing parameter vector', 'It cannot be optimized numerically', 'Every stationary point is a strict local maximum'],
       'Convexity rules out nonglobal local minima; uniqueness needs additional conditions such as strict convexity.', '4.1')
single(c, 'Minibatch SGD', 'How does minibatch stochastic gradient descent reduce the cost of an individual update?',
       'Estimate the gradient from a subset of training examples',
       ['Replace every gradient with zero', 'Use the unseen example\'s true target', 'Require all possible datasets at every update'],
       'A minibatch gradient is cheaper but noisier than a full-batch gradient; overall convergence cost depends on the problem.', '4.2')
matching(c, 'Optimization variants', 'Match each method to the description emphasized in the chapter.',
         [('Minibatch SGD', 'Uses subsets to estimate a gradient'), ('Adagrad', 'Adapts per-parameter learning rates using accumulated squared gradients'),
          ('Momentum', 'Carries update history to accelerate progress and reduce oscillation')],
         'These are optimization procedures, not stand-alone statistical prediction models.', '4.2')
single(c, 'Solver versus learner', 'Why is gradient descent not itself a complete machine-learning algorithm?',
       'It is a general optimizer and does not by itself specify the prediction model, loss, and training task',
       ['It cannot be used to fit a statistical model', 'It is always a clustering method', 'It requires only non-numerical features'],
       'The same optimizer can be used for many different models and objectives, including non-ML problems.', '4.2')
single(c, 'Library workflow', 'What is the practical engineering workflow recommended in the chapter?',
       'Use a well-tested library and check its input, output, and hyperparameter documentation',
       ['Reimplement every optimizer for each task', 'Assume every estimator supports every target type', 'Treat an illustrative code snippet as a complete API specification'],
       'Libraries provide stable implementations, but estimator capabilities and data-shape requirements still matter.', '4.3–4.4')
multiple(c, 'Estimator capabilities', 'Select TWO capabilities to verify before selecting a learning algorithm or implementation.',
         ['Whether it accepts the input feature representation', 'Whether it supports incremental updates from new labeled batches'],
         ['Whether every classifier returns calibrated probabilities by definition', 'Whether every fitted model can be updated without retraining by definition'],
         'Feature support, probability output, class weighting, incremental fitting, and target type vary by estimator.', '4.4')
single(c, 'Class weights', 'What is the intended effect of assigning a larger training weight to a minority class?',
       'Make errors on that class more costly during fitting, potentially trading errors elsewhere',
       ['Guarantee zero error on that class in future data', 'Duplicate the number of input feature columns', 'Turn a classification target into a real-valued regression target'],
       'Weighting changes the optimization tradeoff; it does not guarantee a particular generalization result.', '4.4')
essay(c, 'Debug a training loop', 'A training loop shows rising or oscillating loss after parameter updates. Give a minimal debugging plan grounded in this chapter.',
      'Verify the gradient signs and mean-versus-sum scaling; compute all gradient coordinates at the same current parameters; try a smaller learning rate; track the objective over training. Increasing epochs alone does not fix an unstable update.', '4.2')
essay(c, 'Batch update calculation', 'For one example x=2, y=5, start at w=1, b=1 and use learning rate 0.1. Compute BOTH parameters after one simultaneous MSE gradient step and the new squared error.',
      'Initial residual is 2; gradients are -8 for w and -4 for b; simultaneous updates give w=1.8 and b=1.4; the new prediction is 5 and the squared error is 0.', '4.2')
cards(c, '4.1', [
    ('What three building blocks of a learning algorithm does Chapter 4 name?', 'A loss function, an optimization criterion based on the loss, and an optimization routine using training data.'),
    ('How does per-example loss differ from a training objective?', 'Loss scores a prediction on one example; the objective aggregates losses and may add regularization.'),
    ('What direction does the gradient point toward?', 'The direction of steepest local increase in a differentiable scalar objective under the usual Euclidean geometry.'),
    ('Does convexity imply a unique minimizing parameter vector?', 'No. Every local minimum is global, but multiple minimizers can exist. Strict convexity can give uniqueness when a minimizer exists.'),
])
cards(c, '4.2', [
    ('State the gradient-descent parameter update.', 'theta_new = theta_old - alpha * gradient(objective at theta_old), with positive learning rate alpha.'),
    ('Why does gradient descent subtract the gradient?', 'Because it seeks to reduce the objective, whereas the gradient points toward local increase.'),
    ('If a parameter\'s derivative is negative, how does a gradient-descent step change it?', 'It increases the parameter, since subtracting a negative quantity adds a positive amount.'),
    ('For MSE with prediction w*x+b, what is the derivative with respect to w?', '(-2/N) * sum_i x_i * [y_i - (w*x_i+b)] for a single input feature.'),
    ('For MSE with prediction w*x+b, what is the derivative with respect to b?', '(-2/N) * sum_i [y_i - (w*x_i+b)].'),
    ('At which parameter values should the gradient coordinates for one simultaneous update be evaluated?', 'All at the same old parameter vector, before applying any of that step\'s parameter updates.'),
    ('What is an epoch?', 'One complete traversal or use of the training dataset; it can contain one full-batch update or many minibatch updates.'),
    ('What does the learning rate control?', 'The scale of parameter updates. Too large can cause instability; too small can make learning slow.'),
    ('How does a minibatch gradient differ from a full-batch gradient?', 'It estimates the gradient from a subset of examples, making each update cheaper but typically noisier.'),
    ('What is Adagrad\'s central idea?', 'Use accumulated squared gradients to adapt the step size separately for each parameter.'),
    ('What is momentum\'s central idea in optimization?', 'Carry a history-dependent update direction to speed progress in consistent directions and reduce oscillation.'),
    ('Why is gradient descent a solver rather than a complete prediction model?', 'It optimizes a supplied objective; the model, loss, and data interpretation must be specified separately.'),
    ('Why can parameter initialization matter for gradient-based fitting?', 'For nonconvex objectives it can affect the path and final solution reached. The all-zero initialization in the linear-regression example is not a universal recommendation.'),
    ('Does a small parameter change alone prove that fitting reached the best solution?', 'No. It can indicate convergence, but also an excessively small learning rate or a flat region. Inspect the objective and the broader optimization context.'),
])
cards(c, '4.3–4.4', [
    ('Why do ML engineers generally use libraries rather than implement every learner and optimizer?', 'Libraries provide tested, efficient implementations and supporting tools; engineers can focus on data, modeling choices, and evaluation.'),
    ('What effect can increasing a class weight have?', 'It makes errors on that class more costly during training, shifting the fitted tradeoff; it does not guarantee perfect future classification.'),
    ('What is incremental learning?', 'Updating an existing model from new batches of examples without fitting from scratch on the full history; support depends on the estimator.'),
    ('Before choosing an estimator, what input/output capabilities should you check?', 'Accepted feature types and shapes, supported target tasks, probability or score output, class weights, incremental fitting, and hyperparameters.'),
])


def escape_gift(s):
    return re.sub(r'([\\:#={}~])', r'\\\1', str(s)).replace('\n', r'\n')


def feedback(q):
    return f'{q["explanation"]} Source: section {q["section"]}.'


def gift(q):
    if q['type'] == 'single':
        lines = [('=' if i == q['correct'] else '~') + escape_gift(s)
                 for i, s in enumerate(q['options'])]
    elif q['type'] == 'multiple':
        lines = [('~%50%' if i in q['correct'] else '~%-50%') + escape_gift(s)
                 for i, s in enumerate(q['options'])]
    elif q['type'] == 'numerical':
        lines = [f'#{q["value"]}:{q["tolerance"]}']
    elif q['type'] == 'matching':
        lines = ['=' + escape_gift(a) + ' -> ' + escape_gift(b) for a, b in q['pairs']]
    else:
        lines = []
    lines.append('####' + escape_gift(feedback(q)))
    return '::' + escape_gift(q['title']) + '::' + escape_gift(q['prompt']) + ' {\n    ' + '\n    '.join(lines) + '\n}'


def tsv_line(fields):
    assert all('\t' not in f and '\n' not in f and '\r' not in f for f in fields)
    # Anki supports quoted CSV-style fields with the configured tab separator.
    return '\t'.join('"' + f.replace('"', '""') + '"' for f in fields)


def main():
    quiz_dir = ROOT / 'quizzes' / BOOK_ID
    anki_dir = ROOT / 'anki' / BOOK_ID
    quiz_dir.mkdir(parents=True, exist_ok=True)
    anki_dir.mkdir(parents=True, exist_ok=True)
    header = '#separator:Tab\n#html:true\n#notetype:Basic\n#columns:Front\tBack\tTags\n#tags column:3\n'
    all_rows = []
    key = ['# Answer key — Chapters 1–4', '', 'Spoilers: finish the test before reading. Essay questions require manual self-assessment.', '']
    for ch in CHAPTERS:
        n = ch['number']
        slug = f'chapter-{n:02d}'
        assert len({q['title'] for q in ch['questions']}) == len(ch['questions'])
        text = f'// Original study questions based on Andriy Burkov, 2019.\n$CATEGORY: Chapter {n} — {ch["title"]}\n\n'
        (quiz_dir / f'{slug}.gift').write_text(text + '\n\n'.join(gift(q) for q in ch['questions']) + '\n', encoding='utf-8')
        key += [f'## Chapter {n} — {ch["title"]}', '']
        for i, q in enumerate(ch['questions'], 1):
            if q['type'] == 'single':
                answer = q['options'][q['correct']]
            elif q['type'] == 'multiple':
                answer = '; '.join(q['options'][j] for j in q['correct'])
            elif q['type'] == 'matching':
                answer = '; '.join(f'{a} → {b}' for a, b in q['pairs'])
            elif q['type'] == 'numerical':
                answer = str(q['value'])
            else:
                answer = 'Use the rubric below.'
            key += [f'### {i}. {q["title"]}', '', q['prompt'], '', f'**Answer:** {answer}', '', feedback(q), '']
        rows = []
        for card in ch['cards']:
            front = html.escape(f'HPML Ch {n} — {card["front"]}')
            back = html.escape(card['back']) + '<br><br><small>' + html.escape(f'{BOOK}, Andriy Burkov (2019), §{card["section"]}.') + '</small>'
            tags = f'hpml hpml::ch{n:02d}'
            rows.append(tsv_line([front, back, tags]))
        deck = f'#deck:{BOOK}::Chapter {n:02d} - {ch["title"]}\n'
        (anki_dir / f'{slug}.tsv').write_text(header + deck + '\n'.join(rows) + '\n', encoding='utf-8')
        all_rows.extend(rows)
    (anki_dir / 'chapters-01-04.tsv').write_text(header + f'#deck:{BOOK}::Chapters 01-04\n' + '\n'.join(all_rows) + '\n', encoding='utf-8')
    (STUDY / 'answer-key.md').write_text('\n'.join(key), encoding='utf-8')
    (STUDY / 'source.json').write_text(json.dumps(CHAPTERS, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Built:')
    for ch in CHAPTERS:
        print(f'Chapter {ch["number"]}: {len(ch["questions"])} test questions, {len(ch["cards"])} Anki notes')


if __name__ == '__main__':
    main()
