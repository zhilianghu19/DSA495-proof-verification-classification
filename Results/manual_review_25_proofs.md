# Manual review of 25 ProofWiki proofs

These are the 25 test proofs for which all five models predicted the original dataset label using only the theorem and proof. Manual review retained 18 proof versions (16 labeled Valid and 2 labeled Invalid) and excluded 7. The original label records the dataset judgment. The review decision records whether the proof was kept for the follow-up study.

The entries follow the source row order. Each includes the full theorem and submitted proof. ProofWiki notation is typeset for Markdown. Separate row numbers identify different proofs of the same theorem. [Original records](all_five_correct_test_without_review_reason.json) · [Retained records](manually_reviewed_test_proofs.json)

## Row 69 · Diagonal Relation is Right Identity

**Dataset label** Valid  
**Manual review** Excluded

**Theorem**

Let $\mathcal{R} \subseteq S \times T$ be a relation on $S \times T$.

Then:

$$
\mathcal{R} \circ \Delta_S = \mathcal{R}
$$

where $\Delta_S$ is the diagonal relation on $S$, and $\circ$ signifies composition of relations.

**Submitted proof**

We use the definition of relation equality, as follows:

**Equality of Codomains**

The codomains of $\mathcal{R}$ and $\mathcal{R} \circ \Delta_S$ are both equal to $T$ from Codomain of Composite Relation.

**Equality of Domains**

The domains of $\mathcal{R}$ and $\mathcal{R} \circ \Delta_S$ are also easily shown to be equal.

From Domain of Composite Relation:

$$
\operatorname{Dom} {\mathcal{R} \circ \Delta_S} = \operatorname{Dom} {\Delta_S}
$$

But from the definition of the diagonal relation:

$$
\operatorname{Dom} {\Delta_S} = \operatorname{Img} {\Delta_S} = S
$$

**Equality of Relations**

The composite of $\Delta_S$ and $\mathcal{R}$ is defined as:

$$
\mathcal{R} \circ \Delta_S = \{(x, z) \in S \times T: \exists y \in S: (x, y) \in \Delta_S \land (y, z) \in \mathcal{R}\}
$$

But by definition of the diagonal relation on $S$, we have that:

$$
(x, y) \in \Delta_S \implies x = y
$$

Hence:

$$
\mathcal{R} \circ \Delta_S = \{(y, z) \in S \times T: \exists y \in S: (y, y) \in \Delta_S \land (y, z) \in \mathcal{R}\}
$$

But as $\forall y \in S: (y, y) \in \Delta_S$, this means:

$$
\mathcal{R} \circ \Delta_S = \{(y, z) \in S \times T: (y, z) \in \mathcal{R}\}
$$

That is:

$$
\mathcal{R} \circ \Delta_S = \mathcal{R}
$$

Hence the result.

**Reason for exclusion**

The domain calculation treats the domain of the relation as all of $S$. The set-builder calculation also uses $y$ as both a free and a bound variable.

## Row 73 · Restriction of Mapping to Image is Surjection

**Dataset label** Valid  
**Manual review** Excluded

**Theorem**

Let $f: S \to T$ be a mapping.

Let $g: S \to \operatorname{Img} f$ be the restriction of $f$ to $S \times \operatorname{Img} f$.

Then $g$ is a surjective restriction of $f$.

**Submitted proof**

From Image is Subset of Codomain:

$$
\operatorname{Img} g \subseteq T
$$

Furthermore, by definition of image, we have:

$$
\forall s \in S: g (s) \in \operatorname{Img} g
$$

Therefore, $g$ may be viewed as a mapping $g: S \to \operatorname{Img} g$.

Thus, by definition, $g$ is a surjection.

**Reason for exclusion**

The proof shows that $g$ maps onto its own image. It leaves out the equality $\operatorname{Img} g = \operatorname{Img} f$ needed for the stated codomain.

## Row 75 · Identity Mapping is Bijection

**Dataset label** Valid  
**Manual review** Retained

**Theorem**

The identity mapping $I_S: S \to S$ on the set $S$ is a bijection.

**Submitted proof**

The identity mapping is:

- an injection, from Identity Mapping is Injection

- a surjection, from Identity Mapping is Surjection

and therefore a bijection.

## Row 76 · Bijection iff Left and Right Inverse

**Dataset label** Valid  
**Manual review** Retained

**Theorem**

Let $f: S \to T$ be a mapping.

$f$ is a bijection if and only if:

$$
(1): \quad \exists g_1: T \to S: g_1 \circ f = I_S
$$

$$
(2): \quad \exists g_2: T \to S: f \circ g_2 = I_T
$$

where both $g_1$ and $g_2$ are mappings.

It also follows that it is necessarily the case that $g_1 = g_2$ for such to be possible.

**Submitted proof**

**Necessary Condition**

Let $f: S \to T$ be a mapping.

Let $f$ be such that:

$$
\exists g_1: T \to S: g_1 \circ f = I_S
$$

$$
\exists g_2: T \to S: f \circ g_2 = I_T
$$

where both $g_1$ and $g_2$ are mappings.

Then from Left and Right Inverse Mappings Implies Bijection it follows that $f$ is a bijection.

From Left and Right Inverses of Mapping are Inverse Mapping it follows that:

$$
g_1 = g_2 = f^{-1}
$$

where $f^{-1}$ is the inverse of $f$.

**Sufficient Condition**

Let $f: S \to T$ be a bijection.

Then from Bijection has Left and Right Inverse it follows that:

$f^{-1} \circ f = I_S$ and

$$
f \circ f^{-1} = I_T
$$

where $f^{-1}$ is the inverse of $f$.

## Row 77 · Inverse of Bijection is Bijection

**Dataset label** Valid  
**Manual review** Retained

**Theorem**

Let $f: S \to T$ be a bijection in the sense that:

$(1): \quad f$ is an injection

$(2): \quad f$ is a surjection.

Then the inverse $f^{-1}$ of $f$ is itself a bijection by the same definition.

**Submitted proof**

Let $f$ be both an injection and a surjection.

From Mapping is Injection and Surjection iff Inverse is Mapping it follows that its inverse $f^{-1}$ is a mapping.

From Inverse of Inverse Relation:

$$
(f^{-1})^{-1} = f
$$

Thus the inverse of $f^{-1}$ is $f$.

But then $f$, being a bijection, is by definition a mapping.

So from Mapping is Injection and Surjection iff Inverse is Mapping it follows that $f^{-1}$ is a bijection.

## Row 78 · Inverse Element of Bijection

**Dataset label** Valid  
**Manual review** Retained

**Theorem**

Let $S$ and $T$ be sets.

Let $f: S \to T$ be a bijection.

Then:

$$
f^{-1}(y) = x \iff f(x) = y
$$

where $f^{-1}$ is the inverse mapping of $f$.

**Submitted proof**

Suppose $f$ is a bijection.

Because $f^{-1}$ is a bijection from Bijection iff Inverse is Bijection, it is by definition  a mapping.

The result follows directly from Image of Element under Inverse Mapping.

## Row 79 · Inverse of Inverse of Bijection

**Dataset label** Valid  
**Manual review** Retained

**Theorem**

Let $f: S \to T$ be a bijection.

Then:

$$
(f^{-1})^{-1} = f
$$

where $f^{-1}$ is the inverse of $f$.

**Submitted proof**

A mapping is a relation.

Thus it follows that Inverse of Inverse Relation can be applied directly.

## Row 80 · Inverse of Inverse of Bijection

**Dataset label** Valid  
**Manual review** Retained

**Theorem**

Let $f: S \to T$ be a bijection.

Then:

$$
(f^{-1})^{-1} = f
$$

where $f^{-1}$ is the inverse of $f$.

**Submitted proof**

Let $f: S \to T$ be a bijection.

From Composite of Bijection with Inverse is Identity Mapping we have:

$$
f^{-1} \circ f = I_S
$$

$$
f \circ f^{-1} = I_T
$$

where $I_S$ and $I_T$ are the identity mappings on $S$ and $T$ respectively.

The result follows from Left and Right Inverses of Mapping are Inverse Mapping.

## Row 82 · Composite of Bijections is Bijection

**Dataset label** Valid  
**Manual review** Retained

**Theorem**

Let $f$ and $g$ be mappings such that $\operatorname{Dom} f = \operatorname{Cdm} g$.

Then:

- If $f$ and $g$ are both bijections, then so is $f \circ g$

where $f \circ g$ is the composite mapping of $f$ with $g$.

**Submitted proof**

Let $g: X \to Y$ and $f: Y \to Z$ be bijections.

Then from Bijection iff Inverse is Bijection, both $f^{-1}$ and $g^{-1}$ are bijections.

From Inverse of Composite Relation we have that $g^{-1} \circ f^{-1}$ is the inverse of $f \circ g$.

Then:

$$
(f \circ g) \circ (g^{-1} \circ f^{-1}) = I_Z
$$

$$
(g^{-1} \circ f^{-1}) \circ (f \circ g) = I_X
$$

Hence the result.

## Row 83 · Inverse of Composite Bijection

**Dataset label** Valid  
**Manual review** Retained

**Theorem**

Let $f$ and $g$ be bijections such that $\operatorname{Dom} g = \operatorname{Cdm} f$.

Then:

$$
(g \circ f)^{-1} = f^{-1} \circ g^{-1}
$$

and $f^{-1} \circ g^{-1}$ is itself a bijection.

**Submitted proof**

$\left({g \circ f}\right)^{-1} = f^{-1} \circ g^{-1}$ is a specific example of Inverse of Composite Relation.

As $f$ and $g$ are bijections then by Bijection iff Inverse is Bijection, so are both $f^{-1}$ and $g^{-1}$.

By Composite of Bijections is Bijection, it follows that $f^{-1} \circ g^{-1}$ is a bijection.

## Row 84 · Inverse of Composite Bijection

**Dataset label** Valid  
**Manual review** Retained

**Theorem**

Let $f$ and $g$ be bijections such that $\operatorname{Dom} g = \operatorname{Cdm} f$.

Then:

$$
(g \circ f)^{-1} = f^{-1} \circ g^{-1}
$$

and $f^{-1} \circ g^{-1}$ is itself a bijection.

**Submitted proof**

Let $f: X \to Y$ and $g: Y \to Z$ be bijections.

Then:

$$
(g \circ f) \circ (f^{-1} \circ g^{-1}) = g \circ ((f \circ f^{-1}) \circ g^{-1})
$$

Composition of Mappings is Associative

$$
= g \circ (I_Y \circ g^{-1})
$$

Composite of Bijection with Inverse is Identity Mapping

$$
= g \circ g^{-1}
$$

Identity Mapping is Left Identity

$$
= I_Z
$$

Composite of Bijection with Inverse is Identity Mapping

$$
(f^{-1} \circ g^{-1}) \circ (g \circ f) = (f^{-1} \circ (g^{-1} \circ g)) \circ f
$$

Composition of Mappings is Associative

$$
= (f^{-1} \circ I_Y) \circ f
$$

Composite of Bijection with Inverse is Identity Mapping

$$
= f^{-1} \circ f
$$

Identity Mapping is Right Identity

$$
= I_X
$$

Composite of Bijection with Inverse is Identity Mapping

Hence the result.

## Row 85 · Composite of Permutations is Permutation

**Dataset label** Valid  
**Manual review** Retained

**Theorem**

Let $f, g$ are permutations of a set $S$.

Then their composite $g \circ f$ is also a permutation of $S$.

**Submitted proof**

This follows from the fact that a permutation is a bijection.

The domain and codomain are coincident.

The result follows from Composite of Bijections is Bijection.

## Row 86 · Inverse of Permutation is Permutation

**Dataset label** Valid  
**Manual review** Retained

**Theorem**

If $f$ is a permutation of $S$, then so is its inverse $f^{-1}$.

**Submitted proof**

Let $f: S \to S$ is a permutation of $S$.

By definition, a permutation is a bijection such that the domain and codomain are the same set.

From Bijection iff Inverse is Bijection, it follows $f^{-1}$ is a bijection.

From the definition of inverse relation, the domain of a relation is the codomain of its inverse and vice versa.

Thus the domain and codomain of $f^{-1}$ are both $S$ and it follows that $f^{-1}$ is a permutation.

## Row 87 · Left Inverse Mapping is Surjection

**Dataset label** Valid  
**Manual review** Excluded

**Theorem**

Let $f: S \to T$ be an injection.

Let $g: T \to S$ be a left inverse of $f$.

Then $g$ is a surjection.

**Submitted proof**

Let $f: S \to T$ be an injection.

Then from Injection iff Left Inverse there exists at least one left inverse $g: T \to S$ of $f$ such that $g \circ f = I_S$.

$I_S$ is a surjection.

Thus $g \circ f$ is a surjection.

By Surjection if Composite is Surjection it follows that $g$ is also a surjection.

**Reason for exclusion**

The theorem starts with an arbitrary left inverse. The proof introduces a left inverse by existence without explicitly identifying it with the given one.

## Row 88 · Right Inverse Mapping is Injection

**Dataset label** Valid  
**Manual review** Retained

**Theorem**

Let $f: S \to T$ be a mapping.

Let $g: T \to S$ be a right inverse of $f$.

Then $g$ is an injection.

**Submitted proof**

By the definition of right inverse:

$$
f \circ g = I_T
$$

where $I_T$ is the identity mapping on $T$.

By Identity Mapping is Injection, $I_T$ is an injection.

By Injection if Composite is Injection, it follows that $g$ is an injection.

## Row 390 · Reduced Residue System is Subset of Set of All Residue Classes

**Dataset label** Valid  
**Manual review** Retained

**Theorem**

Let $\mathbb{Z}_m$ be the set of set of residue classes modulo $m$.

Let $\mathbb{Z}'_m$ be the reduced residue system modulo $m$.

Then:

$$
\forall m \in \mathbb{Z}_{> 1}: \varnothing \subset \mathbb{Z}'_m \subset \mathbb{Z}_m
$$

**Submitted proof**

By definition of reduced residue system modulo $m$:

$$
\mathbb{Z}'_m = \{x \in \mathbb{Z}_m: x \perp m\}
$$

From Subset of Set with Propositional Function:

$$
\mathbb{Z}'_m \subseteq \mathbb{Z}_m
$$

We have that:

$$
\gcd \{m, 0\} = m
$$

Thus it follows that:

$$
m > 1 \implies \gcd \{m, 0\} \ne 1
$$

So:

$$
[0]_{m} \notin \mathbb{Z}'_m
$$

However:

$$
[0]_{m} \in \mathbb{Z}_m
$$

so:

$$
\mathbb{Z}'_m \ne \mathbb{Z}_m
$$

Thus:

$$
\mathbb{Z}'_m \subset \mathbb{Z}_m
$$

Then:

$$
[1]_{m} = 1 \implies 1 \perp m
$$

So:

$$
\forall m \in \mathbb{Z}: [1]_{m} \in \mathbb{Z}'_m
$$

Thus:

$$
\mathbb{Z}'_m \ne \varnothing
$$

and therefore:

$$
\varnothing \subset \mathbb{Z}'_m
$$

## Row 391 · Reduced Residue System under Multiplication forms Abelian Group

**Dataset label** Valid  
**Manual review** Retained

**Theorem**

Let $\mathbb{Z}_m$ be the set of set of residue classes modulo $m$.

Let $(\mathbb{Z}'_m, \times)$ denote the multiplicative group of reduced residues modulo $m$.

Then $(\mathbb{Z}'_m, \times)$ is an abelian group, precisely equal to the group of units of $\mathbb{Z}_m$.

**Submitted proof**

From Ring of Integers Modulo m is Ring, $(\mathbb{Z}_m, +, \times)$ forms a (commutative) ring with unity.

Then we have that the units of a ring with unity form a group.

By Multiplicative Inverse in Ring of Integers Modulo m we have that the elements of $(\mathbb{Z}'_m, \times)$ are precisely those that have inverses, and are therefore the units of $(\mathbb{Z}_m, +, \times)$.

The fact that $(\mathbb{Z}'_m, \times)$ is abelian follows from Restriction of Commutative Operation is Commutative.

## Row 394 · Symmetry Group is Group

**Dataset label** Valid  
**Manual review** Excluded

**Theorem**

Let $P$ be a geometric figure.

Let $S_P$ be the set of all symmetries of $P$.

Let $\circ$ denote composition of mappings.

The symmetry group $(S_P, \circ)$ is indeed a group.

**Submitted proof**

By definition, a symmetry mapping is a bijection, and hence a permutation.

From Symmetric Group is Group, the set of all permutations on $P$ form the symmetric group $(\Gamma(P), \circ)$ on $P$.

Thus $S_P$ is a subset of $(\Gamma(P), \circ)$.

Let $A$ and $B$ be symmetry mappings on $P$.

From Composition of Symmetries is Symmetry, $A \circ B$ is also a symmetry mapping on $P$.

Also, by the definition of symmetry, $A^{-1}$ is also a symmetry mapping on $P$.

Thus we have:

$$
A, B \in S_P \implies A \circ B \in S_P
$$

$$
A \in S_P \implies A^{-1} \in \S_P
$$

The result follows from the Two-Step Subgroup Test.

**Reason for exclusion**

The subgroup test requires a nonempty set of symmetries. The proof does not state that the identity mapping is a symmetry of the figure.

## Row 404 · Cauchy's Lemma (Group Theory)

**Dataset label** Valid  
**Manual review** Excluded

**Theorem**

Let $(G, \circ)$ be a group of finite order whose identity is $e$.

Let $p$ be a prime number which divides the order of $G$.

Then $(G, \circ)$ has an element of order $p$.

**Submitted proof**

By the corollary to the First Sylow Theorem, $G$ has subgroups of order $p^r$ for all $r$ such that $p^r \mid \lvert G\rvert$.

Thus $G$ has at least one subgroup $H$ of order $p$.

As a Prime Group is Cyclic, $H$ is a cyclic group.

Thus by definition $H$ has an element of order $p$.

Hence the result.

**Reason for exclusion**

The argument invokes a corollary of the first Sylow theorem. Whether the citation is circular depends on how that theorem was established.

## Row 406 · K-Cycle can be Factored into Transpositions

**Dataset label** Invalid  
**Manual review** Retained

**Theorem**

Every $k$-cycle can be factorised into the product of $k - 1$ transpositions.

This factorisation is not unique.

**Submitted proof**

The cycle $\begin{pmatrix} 1 & 2 & \ldots & k \end{pmatrix}$ has the factorisation:

$$
\begin{pmatrix} 1 & 2 & \ldots & k \end{pmatrix} = \begin{pmatrix} 1 & k \end{pmatrix} \ldots \begin{pmatrix} 1 & 3 \end{pmatrix} \begin{pmatrix} 1 & 2 \end{pmatrix}
$$

Therefore, the general $k$-cycle $\begin{pmatrix} i_1 & i_2 & \ldots & i_k \end{pmatrix}$ has the factorisation:

$$
\begin{pmatrix} i_1 & i_2 & \ldots & i_k \end{pmatrix} = \begin{pmatrix} i_1 & i_k \end{pmatrix} \ldots \begin{pmatrix} i_1 & i_3 \end{pmatrix} \begin{pmatrix} i_1 & i_2 \end{pmatrix}
$$

The cycle $\begin{pmatrix} 1 & 2 & \ldots & k \end{pmatrix}$ also has the factorisation:

$$
\begin{pmatrix} 1 & 2 & \ldots & k \end{pmatrix} = \begin{pmatrix} 1 & 2 \end{pmatrix} \begin{pmatrix} 2 & 3 \end{pmatrix} \ldots \begin{pmatrix} k - 1 & k \end{pmatrix}
$$

Therefore, the general $k$-cycle $\begin{pmatrix} i_1 & i_2 & \ldots & i_k \end{pmatrix}$ also has the factorisation:

$$
\begin{pmatrix} i_1 & i_2 & \ldots & i_k \end{pmatrix} = \begin{pmatrix} i_1 & i_2 \end{pmatrix} \begin{pmatrix} i_2 & i_3 \end{pmatrix} \ldots \begin{pmatrix} i_{k - 1} & i_k \end{pmatrix}
$$

**Original annotation · Invalid inference**

The products exhibit factorizations, but coincide when k=2. The unqualified nonuniqueness claim fails for a transposition written as one transposition.

## Row 409 · Alternating Group is Normal Subgroup of Symmetric Group

**Dataset label** Valid  
**Manual review** Excluded

**Theorem**

Let $n \ge 2$ be a natural number.

Let $S_n$ denote the symmetric group on $n$ letters.

Let $A_n$ be the alternating group on $n$ letters.

Then $A_n$ is a normal subgroup of $S_n$ whose index is $2$.

**Submitted proof**

We have that $\operatorname{sgn}(S_n)$ is onto $C_2$.

Thus from the First Isomorphism Theorem, $A_n$ consists of the set of even permutations of $S_n$.

The result follows from Subgroup of Index 2 is Normal.

**Reason for exclusion**

The proof attributes the description of $A_n$ as the even permutations to the first isomorphism theorem. It also leaves unexplained how $n\ge 2$ ensures that the sign map is onto.

## Row 413 · Condition for Linear Transformation

**Dataset label** Valid  
**Manual review** Excluded

**Theorem**

Let $G$ be a unitary $R$-module, and let $H$ be an $R$-module.

Let $\phi: G \to H$ be a mapping.

Then $\phi$ is a linear transformation if and only if:

$$
\forall x, y \in G: \forall \lambda, \mu \in R: \phi(\lambda x + \mu y) = \lambda \phi(x) + \mu \phi(y)
$$

**Submitted proof**

Any linear transformation clearly satisfies the condition.

Let $\phi$ be such that the condition is satisfied.

Let $\lambda = \mu = 1_R$.

Then $\phi(x + y) = \phi(x) + \phi(y)$.

Now let $\mu = 0_R$.

Then $\phi(\lambda x) = \lambda \phi(x)$.

Thus the conditions are fulfilled for $\phi$ to be a homomorphism, that is, a linear transformation.

**Reason for exclusion**

The additivity step implicitly uses $1_R\phi(x)=\phi(x)$ in $H$. The hypothesis gives this identity by taking $\lambda=1_R$ and $\mu=0_R$, but the proof does not establish it first.

## Row 415 · Submodule Test

**Dataset label** Valid  
**Manual review** Retained

**Theorem**

Let $\left({G, +, \circ}\right)_R$ be a unitary $R$-module.

Let $H$ be a non-empty subset of $G$.

Then $\left({H, +, \circ}\right)_R$ is a submodule of $G$ iff:

$$
\forall x, y \in H: \forall \lambda \in R: x + y \in H, \lambda \circ x \in H
$$

**Submitted proof**

If the conditions are fulfilled, then:

$$
x \in H \implies -x = \left({- 1_R}\right) \circ x \in H
$$

Thus $H$ is a subgroup of $\left({G, +}\right)$ by the Two-Step Subgroup Test, and hence a submodule.

## Row 520 · Comparison Test

**Dataset label** Invalid  
**Manual review** Retained

**Theorem**

Let $\displaystyle \sum_{n \mathop = 1}^\infty b_n$ be a convergent series of positive real numbers.

Let $(a_n)$ be a sequence $\mathbb{R}$ or sequence in $\mathbb{C}$.

Let $\forall n \in \mathbb{N}_{>0}: \lvert a_n\rvert \le b_n$.

Then the series $\displaystyle \sum_{n \mathop = 1}^\infty a_n$ converges absolutely.

**Submitted proof**

Let $\epsilon > 0$.

As $\displaystyle \sum_{n \mathop = 1}^\infty b_n$ converges, its tail tends to zero.

So:

$$
\displaystyle \exists N: \forall n > N: \sum_{k \mathop = n + 1}^\infty b_k < \epsilon
$$

Let $(a_n)$ be the sequence of partial sums of $\displaystyle \sum_{n \mathop = 1}^\infty a_n$.

Then $\forall n > m > N$:

$$
\lvert a_n - a_m\rvert = \lvert (a_1 + a_2 + \cdots + a_n) - (a_1 + a_2 + \cdots + a_m)\rvert
$$

$$
= \lvert a_{m + 1} + a_{m + 2} + \cdots + a_n\rvert
$$

Indexed Summation over Adjacent Intervals

$$
\le \lvert a_{m + 1}\rvert + \lvert a_{m + 2}\rvert + \cdots + \lvert a_n\rvert
$$

Triangle Inequality for Indexed Summations

$$
\le b_{m + 1} + b_{m + 2} + \cdots + b_n
$$

$$
\le \sum_{k \mathop = n + 1}^\infty b_k
$$

$$
< \epsilon
$$

So $(a_n)$ is a Cauchy sequence.

The result follows from Real Number Line is Complete Metric Space or Complex Plane is Complete Metric Space.

**Original annotation · Invalid inference**

The finite tail from m+1 to n is incorrectly bounded by the later tail starting at n+1. Also the Cauchy conclusion is stated for the original partial sums, while absolute convergence concerns the sums of absolute values.

## Row 531 · Multiple of Infimum

**Dataset label** Valid  
**Manual review** Retained

**Theorem**

Let $T \subseteq \mathbb{R}: T \ne \varnothing$ be a non-empty subset of the set of real numbers $\mathbb{R}$.

Let $T$ be bounded below.

Let $z \in \mathbb{R}: z > 0$ be a (strictly) positive real number.

Then:

$$
\displaystyle \inf_{x \mathop \in T}(z x) = z \, \inf_{x \mathop \in T}(x)
$$

where $\inf$ denotes infimum.

**Submitted proof**

From Negative of Infimum is Supremum of Negatives:

$$
\displaystyle -\inf_{x \mathop \in T} x = \sup_{x \mathop \in T}(-x) \implies \inf_{x \mathop \in T} x = -\sup_{x \mathop \in T}(-x)
$$

Let $S = \{x \in \mathbb{R}: -x \in T\}$.

From Negative of Infimum is Supremum of Negatives, $S$ is bounded above.

From Multiple of Supremum:

$$
\displaystyle \sup_{x \mathop \in S}(z x) = z \, \sup_{x \mathop \in S}(x)
$$

Hence:

$$
\displaystyle \inf_{x \mathop \in T}(z x) = -\sup_{x \mathop \in T}(-z x) = -z \, \sup_{x \mathop \in T}(-x) = z \, \inf_{x \mathop \in T}(x)
$$
