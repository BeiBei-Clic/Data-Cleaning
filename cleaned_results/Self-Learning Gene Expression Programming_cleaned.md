IEEE TRANSACTIONS ON EVOLUTIONARY COMPUTATION, VOL. 20, NO. 1, FEBRUARY 2016 65

Self-Learning Gene Expression Programming
Jinghui Zhong, Yew-Soon Ong, and Wentong Cai

Abstract —In this paper, a novel self-learning gene expression programming (GEP) methodology named SL-GEP is proposed to improve the search accuracy and efficiency of GEP. In contrast to the existing GEP variants, the proposed SL-GEP features a novel chromosome representation in which each chromosome is embedded with subfunctions that can be deployed to construct the final solution. As part of the chromosome, the subfunctions are self-learned or self-evolved by the proposed algorithm during the evolutionary search. By encompassing subfunctions or any partial solution as input arguments of another subfunction, the proposed SL-GEP facilitates the formation of sophisticated, higher-order, and constructive subfunctions that improve the accuracy and efficiency of the search. Further, a novel search mechanism based on differential evolution is proposed for the evolution of chromosomes in the SL-GEP. The proposed SL-GEP is simple, generic and has much fewer control parameters than the traditional GEP variants. The proposed SL-GEP is validated on 15 symbolic regression problems and six even-parity problems. Experimental results show that the proposed SL-GEP offers enhanced performances over several state-of-the-art algorithms in terms of accuracy and search efficiency.

Index Terms —Even-parity problem, evolutionary computation, gene expression programming (GEP), genetic programming (GP), symbolic regression problem.

I. INTRODUCTION
GENETIC programming (GP) is an evolutionary computation technique that has been proven to be useful for automating the design of computer programs that solve user-defined tasks [1], [2]. Since its inception by Koza [1], many variants of GP have been developed [3]–[6]. One of the notable variants is gene expression programming (GEP), which was introduced by Ferreira [5]. The distinct feature of GEP is that it adopts a gene expression representation, which models computer programs by using fixed-length strings instead of using parse trees as in the traditional GP. With a gene expression representation, GEP is shown to provide more concise and readable solutions than GP [7]. In the last decade, GEP has been widely used in many applications including classification problems, time series predictions, and others [7]–[11]. However, due to its iterative nature, the GEP can be quite computationally intensive, especially when dealing with large-scale problems. Besides, GEP contains a number of control parameters in the algorithm which require time-consuming fine tuning.

Manuscript received June 13, 2014; revised December 31, 2014; accepted April 5, 2015. Date of publication April 20, 2015; date of current version January 27, 2016. This was supported by the Tier 1 Academic Research Fund under Project RG23/14.
The authors are with the School of Computer Engineering.
###基因表达编程 ###进化计算 ###符号回归 ###自学习 ###差分进化
&&&&
an be quite computationally intensive, especially when dealing with large-scale problems. Besides, GEP contains a number of control parameters in the algorithm which require time-consuming fine tuning.

Manuscript received June 13, 2014; revised December 31, 2014; accepted April 5, 2015. Date of publication April 20, 2015; date of current version January 27, 2016. This was supported by the Tier 1 Academic Research Fund under Project RG23/14.

The authors are with the School of Computer Engineering, Nanyang Technological University, Singapore 639798 (e-mail: jinghuizhong@gmail.com; ASYSOng@ntu.edu.sg; ASWTCAI@ntu.edu.sg).

Digital Object Identifier 10.1109/TEVC.2015.2424410

To enhance the performance of GPs on large-scale and complex applications, an effective approach is to incorporate high-order knowledge that can accelerate the search [12]–[18]. Considering the classical 10-bit even-parity problem, for example, it is extremely difficult for the traditional GP to solve this problem with only primitives “AND,” “OR,” and “NOT.” Nevertheless, if the “XOR” function is introduced as a new primitive, the complexity of the problem can be largely reduced and thus the search process can be significantly accelerated [12]. To define such high-order knowledge, however, is often domain-specific and can be nontrivial.

In the GP community, some efforts to automate the acquisition of high-order knowledge have been reported. For example, Angeline and Pollack [19], as well as Kameya et al. [16], tried to mine for promising partial solutions as high-order knowledge from historical search information, and then ensure their survival during the evolutionary process. Meanwhile, Koza [15] considered the high-order knowledge as forms of automatically defined functions (ADFs) and proposed to evolve ADFs automatically by GP during the evolutionary process. The ADFs are subfunctions that provide subsolutions to specific subproblems. The ADFs can then be combined to provide solutions to larger problems. Thus far, ADFs have been shown to be very effective for improving the performances of GP on a series of problems [15], [20], [21]. Recently, Walker and Miller [22] also considered the use of ADFs in an embedded Cartesian GP (ECGP), which reportedly outperformed GP and GP with ADFs on a variety of problems.

In contrast to the previous studies, little research on incorporating high-order knowledge such as ADFs to enhance GEP have been reported to date. Ferreira [23] had conducted a preliminary research on the use of ADFs to arrive at an enhanced GEP (named GEP-ADF). However, the mechanisms of GEP-ADF make it inefficient or nonscalable to large-scale complex problems. Besides, GEP-ADF has many more new operators and control parameters than the traditional GEP, which makes it inconvenient for practical usage.

To address the mentioned issues, this paper presents a novel self-learning GEP (SL-GEP) methodology. In the proposed SL-GEP, each chromosome is designed to comprise a main
###GEP ###GP ###ADFs ###高阶知识 ###复杂问题
&&&&
Preliminary research on the use of ADFs to arrive at an enhanced GEP (named GEP-ADF). However, the mechanisms of GEP-ADF make it inefficient or nonscalable to large-scale complex problems. Besides, GEP-ADF has many more new operators and control parameters than the traditional GEP, which makes it inconvenient for practical usage.

To address the mentioned issues, this paper presents a novel self-learning GEP (SL-GEP) methodology. In the proposed SL-GEP, each chromosome is designed to comprise a main program and a set of ADFs, all of which are represented using a gene expression approach. Each ADF is then a subfunction for solving a subproblem, and is combined in the main program to solve the given problem of interest. Being part of the chromosome, the ADFs self-learn and are thus automatically designed in the SL-GEP along with the search as evolution progresses online. In the initialization step, all ADFs encoded in each chromosome have been randomly generated. Then in each generation, the evolutionary operators including mutation and crossover shall evolve the ADFs of the chromosomes accordingly. Through the selection operator, ADFs that lead to high-quality solutions are more likely to survive across generations. In this manner, high-quality ADFs are evolved along with the evolutionary search process. A distinct feature of our SL-GEP is that our ADFs encompass other ADFs and/or any subtree of the main program as input arguments, resulting in the formation of complex ADFs or C-ADFs. This feature offers significant flexibility over the classical GEP search as well as the GEP-ADF in the design of sophisticated and constructive ADFs that showcase enhanced accuracy and search efficiency in the search. In addition, a novel search mechanism based on differential evolution (DE) [24] is presented for the effective and efficient evolution of the solution population. The proposed SL-GEP is easy to implement, generic, and contains much fewer control parameters than GEP and GEP-ADF. In the experimental section, the proposed SL-GEP is comprehensively validated using 15 symbolic regression benchmarks and six even-parity problems. Results obtained demonstrate that the SL-GEP outperforms several state-of-the-art GP variants, in terms of accuracy and search efficiency.

The rest of this paper is organized as follows. Section II describes related background techniques. Section III describes the proposed SL-GEP. Section IV presents the experimental studies. At last, Section V draws the conclusion.

II. PRELIMINARIES
This section provides a brief introduction and some background knowledge on the techniques considered in this paper.
###SL-GEP ###ADFs ###GEP-ADF ###进化计算 ###符号回归
&&&&
results obtained demonstrate that the SL-GEP outperforms several state-of-the-art GP variants, in terms of accuracy and search efficiency.

The rest of this paper is organized as follows. Section II describes related background techniques. Section III describes the proposed SL-GEP. Section IV presents the experimental studies. At last, Section V draws the conclusion.

II. PRELIMINARIES

This section provides a brief introduction and some background knowledge on the techniques considered in this paper. In general, GP has been widely used in various applications and one of the most common application areas is symbolic regression [25], [26]. Thus, a formal definition of the symbolic regression problem is presented here to aid readers in comprehending our proposed methodology better. Then the traditional gene expression approach of GEP [5] is presented, followed by a description of the extended gene expression approach that incorporates ADFs as introduced in GEP-ADF [23]. Finally, other related GEP variants are discussed.

A. Symbolic Regression Problem

Given a set of measurement data which consist of input variable values and output responses, the symbolic regression problem involves finding a mathematical formula S(·) to describe the relationships between input variables and the outputs. The mathematical formula S(·) derived can provide insights into the system that generates the data and thus can be subsequently used for predicting the output of new input variables.

Formally, the ith sample data can be expressed as:
[vi,1, vi,2,..., vi,n, oi] (1)
where n is the number of input variables, vi,j is the jth variable value of the ith sample data, and oi is the corresponding output. The formula S(·) is comprised of function symbols (e.g., +, ×, and sin), variables and constants. The quality of S(·) is evaluated by its fitting accuracy for given data. This is commonly achieved using the root-mean-square-error (RMSE).

Fig. 1. Structure of traditional gene expression chromosome.

f(S(·)) = √[Σ(yi - oi)² / N] (2)
where yi is the output of S(·) for the ith input data, oi is the true output of the ith input data, and N is the number of data to be fitted. Therefore, given a function set and variable set as building blocks, the task to solve for a symbolic regression problem is to find the optimal formula S(·)* that minimizes the RMSE for the given data:

S(·)* = arg min S(·) f(S(·)). (3)

B. Traditional Gene Expression Approach of GEP

In traditional GP, the mathematical formula S(·) is represented by tree structures that comprise of two types of nodes: function and terminal. A function node has one or multiple children (e.g., + and sin), while a terminal node is a leaf node without any child (e.g., variables and constants). Instead of using parse trees as in the traditional GP, GEP uses fixed-length strings to represent mathematical formulas. As shown in Fig. 1, a chromosome is represented by a string of symbols.
###SL-GEP ###Symbolic ###Regression ###Gene ###Expression ###Programming ###(GEP) ###RMSE ###Mathematical ###Formula
&&&&
Approach of GEP

In traditional GP, the mathematical formula S(·) is represented by tree structures that comprise of two types of nodes: function and terminal. A function node has one or multiple children (e.g., + and sin), while a terminal node is a leaf node without any child (e.g., variables and constants). Instead of using parse trees as in the traditional GP, GEP uses fixed-length strings to represent mathematical formulas. As shown in Fig. 1, a chromosome is represented by a string of symbols that comprises of two parts, namely Head and Tail. Each element of Head is a function or a terminal, while each element of Tail can only represent a terminal. For example, given a function set:

Ψ1 = {+, −, ∗, /, cos, exp} (4)

and a terminal set:

Γ1 = {x, y} (5)

a typical gene expression chromosome of length 17 can be represented as:

X = [+, −, cos, ∗, x, −, exp, +, y, x, x, x, x, y, x, y, x]. (6)

Each gene expression chromosome can be converted to an equivalent expression tree (ET) using a breadth-first traversal scheme. For example, the chromosome depicted in (6) can be converted to the ET form shown in Fig. 2(a), which can be expressed mathematically as:

(exp(x) ∗ (x + x) − x) + cos(y − x). (7)

The lengths of both Head (h) portion and Tail (l) portion are kept as fixed. In order to ensure that any chromosome can be properly converted into a valid ET, h and l are imposed with the constraint:

l = h · (u − 1) + 1 (8)

where u is the maximum number of children in the functions. For example, if u = 2, then we have l = h + 1.

ZHONG et al.: SL-GEP 67

(a) (b)
Fig. 2. Examples of two ETs. (a) Original ET. (b) Modified ET after mutating a symbol of the original ET.

Fig. 3. Structure of the gene expression chromosome in GEP-ADF.

Note that in each chromosome, there may exist redundant elements in the Tail section, which are not used in the construction of ET in the current search generation. Nevertheless, it is worth noting that these unused elements may become useful in subsequent generations as the search evolves. For instance, referring once again to (6), if the fifth symbol in this chromosome (i.e., x) evolves to +, the 14th and 15th elements (i.e., y and x) change from being deemed as redundant to become useful for constructing the converged ET, which is illustrated in Fig. 2(b). In addition, since the number of nodes in the final ET never exceeds the predefined length of the chromosomes, the gene expression approach has a tendency of producing short programs, thus avoiding the bloating limitation of GP.

In the classic GEP, the evolutionary operators include initialization, evaluation, elitist, selection, mutation, inversion, IS-transposition, root-transposition, one-point crossover, and two-point crossover. The readers are referred to [5] and [8] for the implementation details of GEP.

C. Extended Gene Expression Technique Used in GEP-ADF

Ferreira [23] combined ADF with GEP to arrive at the GEP-ADF. In GEP-ADF, each chromosome consists of a num-
###GEP ###基因表达编程 ###染色体 ###表达式树 ###进化算法
&&&&
thus avoiding the bloating limitation of GP.

In the classic GEP, the evolutionary operators include initialization, evaluation, elitist, selection, mutation, inversion, IS-transposition, root-transposition, one-point crossover, and two-point crossover. The readers are referred to [5] and [8] for the implementation details of GEP.

C. Extended Gene Expression Technique Used in GEP-ADF

Ferreira [23] combined ADF with GEP to arrive at the GEP-ADF. In GEP-ADF, each chromosome consists of a number of conventional genes and a homeotic gene, as illustrated in Fig. 3. All of the conventional genes and the homeotic gene are represented using gene expression. Each conventional gene encodes a sub ET, and serves as an ADF. The homeotic gene fuses different ADFs via linking functions (e.g., + and *), and encodes the main program that generates the final output. The function set and terminal set of ADFs are the same as in the traditional gene expression approach. The function set of the homeotic gene, on the other hand, comprises of the linking functions, while the terminal set of homeotic gene contains only ADFs.

For example, consider the chromosome:
[*,+,−,y,x,x,z,+,/,−,x,y,z,x,*,*,sin,2,+,1,2,1,2,1,2] (9)

Fig. 4. Example chromosome of GEP-ADF and the corresponding ET.

This chromosome encodes two ADFs and one homeotic gene (i.e., the main program). An example ET of the GEP-ADF is illustrated in Fig. 4. It can be observed that both ADF 1 and ADF 2 are used twice in the homeotic gene. Further, it should be noted with this chromosome representation, ADFs can only be used as terminals of the homeotic gene and contain no input argument.

D. Other Related GEP variants

Since the first introduction of GEP, various enhanced GEP variants have been proposed. Existing works mainly focus on hybridizing new operations or adaptive parameter controlling strategies with GEP to improve the search efficiency. For example, Liu et al. [27] proposed an extended GEP which adaptively replaces worse individuals with randomly generated individuals, so as to increase the population diversity. A hybrid selection method was also adopted to improve the search efficiency. Similarly, Zhang and Xiao [28] proposed a modified GEP that dynamically changes the population size (NP) as a way to avoid local stagnation. Instead of first building a tree and then traversing the tree for fitness evaluation, Peng et al. [29] proposed a new method to evaluate fitness of gene expression chromosomes without building the ET. This method was reported to be capable of reducing the computational efforts of the GEP. Bautu et al. [30] presented an adaptive GEP that adaptively adjusts the number of genes used in the chromosomes. Huang [50] studied the schema theory of GEP and developed some theorems that describe the propagation of schema from one generation to another.

In contrast to previous works, this paper extends the canonical GEP with ADFs as part of the chromosome representation.
###GEP ###ADF ###Gene ###Expression ###Chromosome ###Evolutionary ###Operators
&&&&
mes without building the ET. This method was reported to be capable of reducing the computational efforts of the GEP. Bautu et al. [30] presented an adaptive GEP that adaptively adjusts the number of genes used in the chromosomes. Huang [50] studied the schema theory of GEP and developed some theorems that describe the propagation of schema from one generation to another.

In contrast to previous works, this paper extends the canonical GEP with ADFs as part of the chromosome representation that self-evolve or self-learn along with search evolution, while at the same time deploying them for acceleration of the search. Further, this paper develops novel DE-based operators in the GEP. The proposed DE-based search mechanism not only contains much fewer control parameters, but also offers improved search performance.

III. SELF-LEARNING GENE EXPRESSION PROGRAMMING

This section describes the proposed SL-GEP methodology, which is an enhanced version of the classical GEP as well as the GEP-ADF. In contrast to the existing GEP approaches, SL-GEP introduces a novel chromosome representation that facilitates the formation of C-ADFs which embodies sophisticated and constructive high-order knowledge concisely. Further, a novel evolutionary search mechanism is proposed to simplify the evolution of chromosomes in SL-GEP. Since the ADFs and C-ADFs are self-learned along with the GEP search evolution, we label the proposed algorithm as SL-GEP.

A. Proposed Chromosome Representation

In the proposed SL-GEP, each chromosome comprises of a “main program” and several ADFs, as illustrated in Fig. 5. The main program is the compressed expression of the solution, which provides the final output. Meanwhile, each ADF is a subfunction, which can be combined to solve the larger problem in the main program. Both main program and ADFs are represented using a gene expression representation. But the main program and ADFs have different function sets and terminal sets. For the main program, the function set consists of not only functions (e.g., +,−, and sin) but also ADFs defined in the chromosome, while the terminal set consists of variables and constants (e.g., x,y, and π). For ADFs, the function set consists of functions, while the terminal set consists of input arguments. Table I compares and contrasts the function sets and the terminal sets of the three gene expression approaches considered in this paper.

Fig. 6 shows an example chromosome of the proposed representation in SL-GEP. Suppose the value of u in (8) is 2, and h and l are set to be: h=4 and l=5; the head length (h′) TABLE I FUNCTION SETS AND TERMINAL SETS IN THREE GENE EXPRESSION TECHNIQUES
###GEP ###SL-GEP ###染色体表示 ###ADFs ###搜索性能
&&&&
and π). For ADFs, the function set consists of functions, while the terminal set consists of input arguments. Table I compares and contrasts the function sets and the terminal sets of the three gene expression approaches considered in this paper.

Fig. 6 shows an example chromosome of the proposed representation in SL-GEP. Suppose the value of u in (8) is 2, and h and l are set to be: h=4 and l=5; the head length (h') and tail length (l') of ADFs are set to be: h'=3 and l'=4.

TABLE I
FUNCTION SETS AND TERMINAL SETS IN THREE GENE EXPRESSION TECHNIQUES

A typical chromosome with one ADF can be expressed as:
[G, sin, G, G, x, π, x, z, y, *, +, *, a, b, a, b] (10)
where {+, *, sin} is the function set, G is the ADF, {x, z, π} is the terminal set, and {a, b} is the set of input arguments.

As shown in Fig. 6, the main program can be decoded as:
G(sin(G(x,z)), G(x,π)) (11)

and the ADF can be decoded as:
G(a,b) = (a+b) * (a*b). (12)

Inserting (12) into (11), we then obtain the final expression (S):
S = G(sin(G(x,z)), G(x,π))
= G(sin((x+z)*(x*z)), (x+π)*(x*π))
= (sin((x+z)*(x*z)) + (x+π)*(x*π))) * (sin((x+z)*(x*z)) * (x+π)*(x*π))). (13)

In this way, an ET with 33 nodes can be concisely represented by two ETs with a total of only 15 nodes. Through this simple example, we hope to demonstrate the benefit of the proposed chromosome representation in terms of effectively compressing complex expressions concisely.

In addition, as can be seen in the above example, a distinct feature of the SL-GEP that differs from GEP-ADF [23] is that our approach introduces C-ADFs that have input arguments that can come in the form of variables (e.g., x and z), constants (e.g., π), ADFs, or any subtree of the main program. For example, in Fig. 6(a), the root node of the main program is an ADF with two input arguments. The first input argument is a subtree of the main program [i.e., sin(G(x,z))], while the second input argument is an ADF [i.e., G(x,π)]. This feature significantly improves the capabilities of chromosomes to represent sophisticated high-order expressions concisely. Specifically, the expression x^100 can be represented as G*G*G*G*G*G*G*G*G*G, when G=x^10 and * are defined as the ADF and linking function, respectively, in the GEP-ADF. In contrast, the same expression can be more concisely represented as G(G(x)) in our proposed SL-GEP by simply defining a C-ADF with G(a)=a^10. This is not only more concise but also more human readable.

B. Proposed Algorithm
The chromosome representation of SL-GEP is of fixed length and structurally similar to the traditional gene expression. Thus, the search mechanism of GEP can be easily integrated to evolve chromosomes with the proposed representation. However, the GEP contains a number of operations and control parameters that need to be carefully tuned. To solve this problem and further improve the performance, this section proposes a novel search mechanism based on DE oper-.

ZHONG et al.: SL-GEP 69
TABLE II
BASIC NOTATIONS
###SL-GEP ###ADFs ###染色体表示 ###基因表达 ###表达式压缩
&&&&
representation of SL-GEP is of fixed length and structurally similar to the traditional gene expression. Thus, the search mechanism of GEP can be easily integrated to evolve chromosomes with the proposed representation. However, the GEP contains a number of operations and control parameters that need to be carefully tuned. To solve this problem and further improve the performance, this section proposes a novel search mechanism based on DE operations. The procedure of the proposed SL-GEP is given in Algorithm 1, which consists of four main steps, namely initialization, mutation, crossover, and selection. The basic notations are listed in Table II.

1) Step 1—Initialization: The first step is to generate NP random chromosomes to form an initial population. As defined in Section III-A, each chromosome can be represented by a vector of symbols labeled here as target vector:
X_i = [x_i,1, x_i,2,..., x_i,D] (14)
where i is the index of the chromosome in the population, D is the length of the chromosome, and x_i,j is the jth element of X_i. The value of D is computed by:
D = h + l + K * (h' + l') (15)
where K is the number of ADFs in each chromosome. Note that in this paper, the maximum number of input arguments for all functions and ADFs is two, thus we have l = h+1, and l' = h'+1. The value of x_i,j is assigned by a “random assignment” scheme which contains two phases. The first phase is to configure the type as a function, ADF, terminal, or input argument, randomly. Nevertheless, the assigned type must be feasible. For example, if x_i,j belongs to the Tail of a main program, then x_i,j can only be of a terminal type. Denoting the set of feasible values of the assigned type as E, the second phase thus involves a random selection of a feasible value from E as the value of x_i,j.

It should be noted that the initialization step randomly initializes the chromosomes, including the ADFs. The chromosomes are then evolved iteratively via the mutation, crossover and selection evolutionary operations. Hence, the ADFs will self-learn along with the SL-GEP search, without a priori knowledge or manual configuration.

Algorithm 1: SL-GEP
1 Begin:
2 for i = 1 to NP do
3  for j = 1 to D do
4   x_i,j ← “random assignment”
5 Evaluate the initial population
6 while termination condition is not met do
7  Update the frequencies of functions and variables
8  for i = 1 to NP do
   /* mutation and crossover */
9   F = rand(0,1); CR = rand(0,1)
10  Randomly choose two individuals X_r1 ≠ X_i, and X_r2 ≠ X_i ≠ X_r1 from current population
11  Set k to be a random integer between 1 and D
12  for j = 1 to D do
13   Calculate the mutation probability φ by (28)
14   if (rand(0,1) < CR or j = k) and (rand(0,1) < φ) then
15    u_i,j ← “frequency-based assignment”
16   else
17    u_i,j = x_i,j
   /* Selection */
18  if f(U_i) < f(X_i) then
19   X_i = U_i;
20 End

2) Step 2—Mutation: In the second step, a mutation operation is performed on each target vector to generate a mutant.
###SL-GEP ###基因表达式编程 ###进化算法 ###染色体 ###变异
&&&&
feasible value from
Eas the value of xi,j.
It should be noted that the initialization step randomly
initializes the chromosomes, including the ADFs. The chromo-
somes are then evolved iteratively via the mutation, crossover
and selection evolutionary operations. Hence, the ADFs will
self-learn along with the SL-GEP search, without a priori
knowledge or manual configuration.
2) Step 2—Mutation: In the second step, a mutation oper-
ation is performed on each target vector to generate a mutant
vector. The traditional DE mutation is expressed as
Yi=Xr1+F·(Xr2−Xr3) (16)
where F is the scaling factor and r1,r2,r3, and i are four
distinct individual indices.
However, since the elements in the chromosomes are
discrete symbols, the numerical operations of the tradi-tional DE cannot be directly used. To address this issue,
we decompose the DE mutation into three phases. The
first phase is to obtain a difference (Δ1) of two random
target vectors in the current population (named distance
measuring)
Δ1=(Xr2−Xr3). (17)
The second phase is to scale the difference by a coefficient F
(named distance scaling)
Δ1'=F·Δ1. (18)
70 IEEE TRANSACTIONS ON EVOLUTIONARY COMPUTATION, VOL. 20, NO. 1, FEBRUARY 2016
The third phase is to add the scaled difference to another ran-
dom target vector to create a mutant vector (named distance
adding)
Yi=Xr1+Δ1'. (19)
In the search space of tree structure computer programs, the
above three phases are implemented as follows.
a) Distance measuring: In the discrete domain, the dis-
tance between two elements can be zero (i.e., two elements
are the same) or non-zero. Here we use a “don’t care” symbol
“*” to represent a non-zero distance
xi,j−xk,j={
0,if xi,j is the same as xk,j
*,otherwise (20)
where xi,j and xk,j are the jth element value of Xi and the jth
element value of Xk, respectively. For example, sin −exp=*;
sin−sin=0. In this way, we can obtain the Δ1 in (17) using
a binary difference vector. Each dimension of the difference
vector is then computed using (20).
b) Distance adding: We describe the third phase before
the second phase to facilitate the understanding. The third
phase adds a difference vector to a target vector, so as to create
a mutant vector. Clearly, an element will remain unchanged if
it is added to a zero distance
xi,j+0=xi,j. (21)
If xi,j is added to a non-zero distance, it will evolve into a new
value
xi,j+*= a, a∈Ω1j (22)
where Ω1j is the set of feasible values for the jth dimension
of Xi. The new value a is selected with a “frequency-based
assignment” scheme, as described in Algorithm 2. In the
frequency-based assignment scheme, if xi,j∈ADF, it will
be assigned in the same way as in the random assignment
scheme. Otherwise, the type is chosen based on the frequencies
of the feasible types that appear in the population. Particularly,
feasible types that appear more often in the population are
###DE ###mutation ###差分进化 ###基因表达式编程 ###变异操作 ###距离测量
&&&&
a, a ∈ Ω1j (22)
where Ω1j is the set of feasible values for the jth dimension of Xi. The new value a is selected with a “frequency-based assignment” scheme, as described in Algorithm 2. In the frequency-based assignment scheme, if xi,j ∈ ADF, it will be assigned in the same way as in the random assignment scheme. Otherwise, the type is chosen based on the frequencies of the feasible types that appear in the population. Particularly, feasible types that appear more often in the population are more likely to be selected when using the frequency-based assignment scheme. The selection probability of a is
pa = (ca + c0) / Σb∈Ω1j (cb + c0) (23)
where ca is the frequency of a in the main programs of all chromosomes in the population, and c0 is a small constant (e.g., c0 = 1). We introduce c0 to ensure that each feasible value has at least a small selection probability even though its frequency is near to zero or equals zero.

c) Distance scaling: In the second phase, the difference vector is scaled by a coefficient factor F. To achieve this, we make xi,j evolve into a new value at a mutation probability of φ, if it is added to a nonzero distance. The mutation probability is determined by
φ = Σa∈Ω1j [F · (ca + c0) / Σb∈Ω1j (cb + c0)] = F. (24)

**Algorithm 2: Frequency-Based Assignment**
**Input:** The element to be mutated (I).
**Output:** The mutated element (I).
1 Begin:
2 if I ∈ H1 then
3  if rand(0,1) < θ then
4   I = Roulette-wheel(function set ∪ ADF set).
5  else
6   I = Roulette-wheel(terminal set)
7 else if I ∈ T1 then
8  I = Roulette-wheel(terminal set)
9 else if I ∈ H2 then
10  type = Rand ({function, input argument})
11  if type = function then
12   I = Rand (function set)
13  else
14   I = Rand(input argument set)
15 else if I ∈ T2 then
16  I = Rand(input argument set)
17 End

In this way, a small F translates to a small mutation probability, which has the effect of making the mutant vector more similar to the base target vector.

To summarize, the above three phases enable the DE mutation to generate mutant vectors in a discrete space. In the SL-GEP, we use the commonly used “DE/current-to-best/1” mutation scheme as expressed by
Yi = Xi + F · (Xbest - Xi) + F · (Xr1 - Xr2) (25)
where Xbest is the best individual in the population. The above mechanism can be easily extended to implement the DE/current-to-best/1. The computation process of (25) can be decomposed into two substeps, i.e., Ti = Xi + F · (Xbest - Xi) and Yi = Ti + F · (Xr1 - Xr2), where Ti = [ti,1, ti,2,..., ti,n] is a temporary vector. The probabilities of xi,j and ti,j remaining unchanged in the first and second substep are 1 - F · ψ(xpbest,j, xi,j) and 1 - F · ψ(xr1,j, xr2,j), respectively, where ψ(a,b) is defined as
ψ(a,b) = { 1, if a ≠ b
         { 0, otherwise. (26)
Therefore, the probability of xi,j remaining unchanged after performing the two substeps is
(1 - F · ψ(xbest,j, xi,j)) * (1 - F · ψ(xr1,j, xr2,j)). (27)
###频率分配 ###变异概率 ###差分进化 ###距离缩放 ###基因表达式编程
&&&&
temporary vector. The probabilities of xi,j and ti,j remaining unchanged in the first and second substep are 1 − F · ψ(xpbest,j, xi,j) and 1 − F · ψ(xr1,j, xr2,j), respectively, where ψ(a,b) is defined as:
ψ(a,b) = {
  1, if a ≠ b
  0, otherwise
} (26)

Therefore, the probability of xi,j remaining unchanged after performing the two substeps is:
(1 − F · ψ(xbest,j, xi,j)) * (1 − F · ψ(xr1,j, xr2,j)) (27)

Hence, the mutation probability of xi,j is:
ϕ = 1 − (1 − F · ψ(xbest,j, xi,j)) * (1 − F · ψ(xr1,j, xr2,j)) (28)

To improve the robustness of the algorithm and reduce the number of control parameters, we also adopt a random scheme ZHONG et al.: SL-GEP 71 to set the values of F in the DE/current-to-best/1 mutation scheme:
F = rand(0,1) (29)
where rand(a,b) returns a random value uniformly distributed within [a,b].

3) Step 3—Crossover: In the third step, each target vector Xi is crossover with its mutant vector Yi to create a trial vector Ui:
ui,j = {
  yi,j, if rand(0,1) < CR or j = k
  xi,j, otherwise
} (30)
where CR is the crossover rate, k is a random integer between 1 and D, and ui,j, yi,j and xi,j are the jth variables of Ui, Yi, and Xi, respectively. Similar to F, the value of CR is set to be CR = rand(0,1).

4) Step 4—Selection: Finally, in the fourth step, the fitter solution between each pair of the target and trial vector is then chosen to form a new population:
Xi = {
  Ui, if f(Ui) < f(Xi)
  Xi, otherwise
} (31)
where f(X) returns the fitness value of X.

There is a repetition between the second step and the fourth step until the termination condition is met.

To summarize, the above four steps extend the DE search mechanism to evolve the encoded solutions. It should be noted that the proposed SL-GEP is a generic framework such that other state-of-the-art DEs such as JADE [31], CoDE [32], and others [33], [34] can be easily used as alternatives. In what follows, we study the proposed algorithm with GEP and GEP-ADF in terms of their computational complexities and control parameter sizes. According to the above procedures, the computational complexity of the proposed SL-GEP in each generation is the sum of two parts: 1) generating NP new chromosomes and 2) decoding the NP new chromosomes into the ETs and evaluating their fitness values. The frequencies of functions and variables can be updated by scanning the elements in the population with a single pass, which has a complexity of O(NP·D). Selecting one element based on the frequency-based assignment scheme is a roulette-wheel selection procedure. By using the method proposed in [35], the complexity of the above frequency-based assignment operation can be reduced to O(1). Thus, the complexity for mutation and crossover is O(NP·D), and the complexity of the first part is O(NP·D). The complexity of the second
###SL-GEP ###变异概率 ###交叉操作 ###选择机制 ###计算复杂度
&&&&
Variables can be updated by scanning the elements in the population with a single pass, which has a complexity of O(NP·D). Selecting one element based on the frequency-based assignment scheme is a roulette-wheel selection procedure. By using the method proposed in [35], the complexity of the above frequency-based assignment operation can be reduced to O(1). Thus, the complexity for mutation and crossover is O(NP·D), and the complexity of the first part is O(NP·D). The complexity of the second part is problem-specific but is the same for all GEP variants. Denoting the complexity of the second part as O(f), then the complexity of the proposed SL-GEP for each generation is O(NP·D)+O(f). Accordingly, we can obtain the complexity of GEP and GEP-ADFs as O(NP·D)+O(f). Thus, the complexities of our proposed SL-GEP algorithm, GEP and GEP-ADF are similar. Meanwhile, as listed in Table III, the proposed SL-GEP algorithm has only four control parameters, while the standard GEP and GEP-ADF contain eleven control parameters and twenty control parameters, respectively. From this point of view, the proposed SL-GEP algorithm contains much fewer control parameters and thus is more convenient and appropriate for practical usage.

**C. Constant Creation**
Numerical constant is an integral part of most mathematical formulas. Hence, the creation of numerical constants is an important part of GP and its variants toward the evolution of satisfying mathematical formulas. However, it is rather challenging for GP-like methods to precisely approximate the constant values, because the numerical constants are continuous values while the chromosome representations of GP-like methods are generally suitable for combinatorial optimization. In the literature, several methods have been proposed for solving the constant creation problem. The most common one is the “ephemeral random constant (ERC)” which was introduced by Koza [1]. In Koza’s method, the ERC is treated as a special terminal symbol. The value of each ERC is assigned with a random value within a specific range when creating the initial population. Then the random ERCs are fixed and moved from one parse tree to another by the crossover operator. Ferreira [36] proposed a new method to handle constants in GEP. In Ferreira’s method, an extra terminal “?” is used to represent constants in the formula. A constant pool is randomly created and assigned to each individual in the initialization. When decoding the gene expression chromosome for fitness evaluation, each ? is assigned with a constant in the constant pool accordingly. An extra dc domain and some special dc operations are introduced to facilitate the constant creation process. Besides the above two methods, others such as the local search method [37], nonlinear least squares minimization [38], and EAs [39] have also been used to search for constant values.
###SL-GEP ###GEP ###复杂度 ###常量创建 ###控制参数
&&&&
Newly created and assigned to each individual in the initialization. When decoding the gene expression chromosome for fitness evaluation, each constant is assigned with a constant in the constant pool accordingly. An extra DC domain and some special DC operations are introduced to facilitate the constant creation process. Besides the above two methods, others such as the local search method [37], nonlinear least squares minimization [38], and EAs [39] have also been used to search for constant values.

As in GEP [8], the constant creation operation is regarded as an optional operation in the proposed SL-GEP. When constants are considered in the search process, the SL-GEP adopts the commonly used ERC to handle constants, due to its simplicity. It should be noted that other existing constant handling methods can also be considered in the proposed SL-GEP with ease. Specifically, a set of fixed random constants within a specific range (e.g., [-1, 1]) have been generated in the initialization step. A new terminal symbol is introduced to represent ERCs. In the random-assignment and the frequency-based assignment procedures, each element of H1 and T1 has probability of being assigned with a constant. When an element is to be assigned with a constant, a random constant from the constant set will be selected. The constant assigned to the element shall remain fixed for the rest of the run unless a frequency-based assignment mutation is performed on it.

72 IEEE TRANSACTIONS ON EVOLUTIONARY COMPUTATION, VOL. 20, NO. 1, FEBRUARY 2016

TABLE IV
FIFTEEN SYMBOLIC REGRESSION BENCHMARKS FOR VALIDATION

IV. EXPERIMENTS AND COMPARISONS
This section investigates the performance of the proposed SL-GEP. First, the experiment settings, including the benchmark test problems and the performance metrics for comparison are presented. Then, the proposed SL-GEP is assessed against GEP, GEP-ADF, GP and two recently published GP variants. Finally, the impacts of important control parameters of SL-GEP are investigated.

A. Experimental Settings
This section assesses the performance of SL-GEP via solving two categories of well-established problems. The first category contains 15 symbolic regression problems, as listed in Table IV. These benchmark problems are chosen from [26] and [40]. Among them, F1–F14 are commonly used benchmark problems that have unique structural complexities with respect to the objective formulas. F15 emerges from an industrial problem on modeling gas chromatography measurements of the composition of a distillation tower. This problem contains 4999 records, with each record containing 25 potential input variables and one output value.

In Table IV, the last column describes the dataset to be fitted, where U[a,b,c] represents c uniform random samples from a to b. As suggested in [26], the function set of all 15 problems is set to be {+,−,×,÷,sin,cos,ex,ln(|x|)}.

The second category is the k-even-parity problem, which...
###SL-GEP ###常量处理 ###符号回归 ###基因表达编程 ###实验设置
&&&&
lemon modeling gas chromatography measurements of the composition of a distillation tower. This problem contains 4999 records, with each record containing 25 potential input variables and one output value.

In Table IV, the last column describes the dataset to be fitted, where U[a,b,c] represents c uniform random samples from a to b. As suggested in [26], the function set of all 15 problems is set to be {+,−,×,÷,sin,cos,ex,ln(|x|)}.

The second category is the k-even-parity problem, which requires finding a suitable boolean formula comprising k arguments. The boolean formula should return true value if and only if there are even number of arguments assigned with true values. The even-parity problems are popular benchmark problems for assessing GP [26]. These are very difficult boolean optimization problems for blind random search and the traditional GP. In this paper, six even-parity problems are considered in the second category, i.e., three-parity to eight-parity problems. As suggested in [22], the function set of the six even-parity problems is set to be {AND,OR,NAND,NOR}.

Seven GP variants have been chosen to pit against the proposed SL-GEP. The first algorithm is the traditional GEP [5]. The second algorithm is the GEP-ADF [23], which is a preliminary version of GEP combined with ADF. The third is the GP system developed based on the ECJ library [41]. The fourth is LDEP [42], which combines DE with linear GP. The fifth is the Tree-based DE (TreeDE) [43], a discrete version of DE for solving symbolic regression problems. The sixth is a modified SL-GEP named GEP-ADF2, which replaces the proposed DE-based search mechanism with the traditional operations of GEP (e.g., selection, mutation, one-point crossover, and two-point crossover). We compare SL-GEP with GEP-ADF2 to analyze the effectiveness of the proposed DE-based search mechanism. The last one is an enhanced version of SL-GEP (labeled as SL-GEP/JADE), which replaces the classical DE/current-to-best/1 mutation strategy in SL-GEP with the DE/current-to-pbest/1 strategy in JADE [31]. The self-adaptive parameter control strategy of JADE is also adopted in SL-GEP/JADE to adaptively adjust F and CR. We introduce SL-GEP/JADE simply to demonstrate that the proposed SL-GEP provides a generic framework where different search mechanisms can be easily accommodated.

Table V lists the parameter settings of the algorithms under consideration. The parameters of TreeDE and LDEP are configured according to what have been suggested in their original papers. As suggested in [44], the NP of GP is set to be 1024, and other parameters are set the same as the default settings in the ECJ library. The parameters of GEP and GEP-ADF are set as suggested by Ferreira in [23].
###SL-GEP ###GP ###Even-parity ###problems ###Symbolic ###regression ###GEP ###variants
&&&&
mechanisms can be easily accommodated.
Table V lists the parameter settings of the algorithms under consideration. The parameters of TreeDE and LDEP are configured according to what have been suggested in their original papers. As suggested in [44], the NP of GP is set to be 1024, and other parameters are set the same as the default settings in the ECJ library. The parameters of GEP and GEP-ADF are set as suggested by Ferreira in [23]. In the original paper of GEP and GEP-ADF, the author did not suggest a fixed rule for setting the head length, but suggested using different head lengths for solving different kinds of problems. As a rule of thumb, the larger number of variables a problem has, a larger head length should be used. In our experimental studies, the head length is set empirically based on the variable size of the problem. For fair comparison, we fixed the head lengths of all GEP variants to be 10 for solving small variable size problems such as F1-F14, while 20 for solving large size problems like F15 and the six even-parity problems. As for LDEP, the suggested number of registers is 6 which is infeasible for solving large-scale even-parity problems and F15, where the numbers of variables are larger than 6. To solve this issue, the number of registers of LDEP is set to 12 for the six even-parity problems and 40 for F15. Our experimental studies showed that these settings produced promising results. To solve problems that require constants (i.e., F13, F14, and F15), GP used Koza’s ERC that was implemented in the ECJ library, while GEP, GEP-ADF, and GEP-ADF2 used Ferreira’s method as described in [8]. The LDEP used the special constant creation mechanism as proposed in its original paper, and our proposed SL-GEP and SL-GEP/JADE considered the method described in Section III-C. For all problems, each algorithm will terminate when the number of evaluations reaches a maximum of 1,000,000 (i.e., Emax=1,000,000).

B. Performance Metrics for Comparison
For the 15 symbolic regression problems, the tenfold cross validation method is adopted for training and testing. Specifically, for each problem, the dataset is evenly divided into tenfold. For each EA run, ninefold are used for training while the remaining fold is used at the end to test the best solution found. There are ten different cases, and we repeated each algorithm on each case for ten times with different random seeds. Hence, there are altogether 100 different runs for each algorithm on each problem. During the training stage, ninefold of data are used to evaluate the fitness of each solution, as in (2). When an algorithm converges to a solution Si with f(Si)<10^-4, a successful search convergence or perfect hit is assumed. At the end of each EA run, the best solution attained is tested using (2) based on the remaining fold of data. The average testing result of the 100 EA runs is used for comparison analysis. As for the six even-parity problems,
###算法参数 ###性能评估 ###遗传编程 ###符号回归 ###交叉验证
&&&&
nt runs for each algorithm on each problem. During the training stage, ninefold of data are used to evaluate the fitness of each solution, as in (2). When an algorithm converges to a solution Si with f(Si)<10−4, a successful search convergence or perfect hit is assumed. At the end of each EA run, the best solution attained is tested using (2) based on the remaining fold of data. The average testing result of the 100 EA runs is used for comparison analysis. As for the six even-parity problems, the training data are all possible input assignments and the corresponding outputs. For example, the three-parity problem contains 2^3=8 different input and output pairs. These eight input and output pairs are used as the training data. The fitness value of each solution is evaluated based on (2) using all the training data. Since there is no testing data for even-parity problems, for each algorithm we performed 100 independent runs on each problem. The average training performances of the 100 runs are then reported.

In the empirical studies, the first performance metric considered is the testing accuracy given by (2). This metric is regarded as most important for evaluating the performance of an algorithm. Besides, as suggested in [45], the success rate of achieving perfect hits (denoted as Suc) is adopted as the second metric. The Suc is computed by:

Suc = Cs / C * 100% (32)

where C is the number of independent runs and Cs is the number of successful runs achieving a perfect hit.

In addition, the number of fitness evaluations required to achieve a perfect hit (denoted as run time, RT) is adopted as the third performance metric. This metric gives an indication of the convergence speed of an algorithm. In the event an algorithm fails to achieve a perfect hit, the method described in [46] is then considered for estimating the RT:

RT = Es + 1 - Suc / Suc * Emax (33)

where Es is the average number of fitness evaluations to achieve a perfect hit for the successful runs and Emax is the maximum number of fitness evaluations.

C. Comparisons With GEP and GEP-ADF2

Table VI summaries the Suc and RMSE obtained by GEP, GEP-ADF2 and SL-GEP. The RMSE is the average testing accuracy of the 100 independent runs based on tenfold cross-validation. For each problem, a Wilcoxon signed-rank test is performed to detect for significant differences between two algorithms. First, we evaluate our GEP-ADF2 against the conventional GEP [5]. It can be observed from Table VI that GEP-ADF2 significantly outperformed GEP on 11 out of the 21 problems according to the RMSE, and performed competitively on the remaining ten problems. Especially, GEP-ADF2 reported much higher Suc on all six even-parity problems, while GEP failed to locate the global optimum for the last.

TABLE VI: COMPARISON RESULTS OF GEP, GEP-ADF2, AND SL-GEP
74 IEEE TRANSACTIONS ON EVOLUTIONARY COMPUTATION, VOL. 20, NO. 1, FEBRUARY 2016
TABLE VII: EXAMPLE ADF SFOUND BY GEP-ADF2 ON F1–F6 AND THE SIX EVEN-PARITY PROBLEMS
###GEP-ADF2 ###性能评估 ###成功率 ###运行时间 ###偶校验问题
&&&&
It can be observed from Table VI that GEP-ADF2 significantly outperformed GEP on 11 out of the 21 problems according to the RMSE, and performed competitively on the remaining ten problems. Especially, GEP-ADF2 reported much higher Suc on all six even-parity problems, while GEP failed to locate the global optimum for the last four problems. This is because the solution expression of a large-scale even-parity problem becomes overwhelming or extremely complex. Thus, such problems are very difficult for the traditional GEP to solve, especially without the use of subfunctions.

Besides the even-parity problems, GEP-ADF2 also exhibited better performances on problems F2–F6. Further analysis and verifications indicated that these are the kind of problems whose solutions can be compressed effectively with the use of ADFs. For example, the original expression of F5 is “x\*x\*x\*x\*x+x\*x\*x\*x+x\*x\*x+x\*x+x,” which contains 29 symbols. By using “G(a,b)=b+b\*a” as an ADF, F5 can be compressed as “G(G((x\*x),G(x,x)),x),” which contains much fewer symbols. Table VII showcases several other solutions found by GEP-ADF2 on problems F1–F6 and the six even-parity problems. It is worth noting that the converged solutions are found to be very concise, which is made possible due to the use of ADFs. Note that GEP-ADF2 needs additional computational requirements to search for the promising ADFs. Hence, on simple problems such as F4 and F1, the benefit of using ADFs is not very significant. However, as the complexity of the problem increases, the benefit of ADFs becomes more evident and significant, as can be observed from the results of F5, F6, as well as the six even-parity problems. As for F7−F12, their original expressions contain only a few number of symbols. Thus, they can be expressed concisely without using ADFs. Thus, the performances of GEP-ADF2 are similar to those of GEP on these problems. These results demonstrate that the proposed GEP-ADF2 can effectively utilize the ADFs in improving the search accuracy of GEP.

Next, we evaluate SL-GEP against GEP-ADF2 to investigate the effectiveness of the proposed DE-based search mechanism for discrete problems. It can be observed that SL-GEP performed significantly better than GEP-ADF2 on 12 problems, and performed competitively on the remaining nine problems, in terms of the RMSE. However, according to the Suc values, SL-GEP obtained 100% success rate on 12 problems, which is superior to the GEP-ADF2. Besides, the Suc values of SL-GEP on the remaining nine problems were observed to be much better than or at least competitive to those of GEP-ADF2. These results thus indicate that the proposed DE-based search mechanism helps to further improve the performance of GEP-ADF2.
###GEP-ADF2 ###ADFs ###SL-GEP ###性能比较 ###问题复杂度
&&&&
ADF2 on 12 problems, and performed competitively on the remaining nine problems, in terms of the RMSE. However, according to the Suc values, SL-GEP obtained 100% success rate on 12 problems, which is superior to the GEP-ADF2. Besides, the Suc values of SL-GEP on the remaining nine problems were observed to be much better than or at least competitive to those of GEP-ADF2. These results thus indicate that the proposed DE-based search mechanism helps to further improve the performance of GEP-ADF2.

In addition, we also perform the multiple-problem Wilcoxon’s test to check the behaviors of GEP, GEP-ADF2, and SL-GEP on the test suite. Table VIII summarizes the statistical results. Again, the results of the multiple-problem Wilcoxon’s test indicate that the GEP-ADF2 exhibited significantly better performance than GEP, while the proposed SL-GEP exhibited significantly better performance than both GEP and GEP-ADF2, with a probability error of p<0.05.

D. Comparisons With Other GP Variants
This section evaluates the results of SL-GEP against the GP, GEP-ADF, TreeDE, LDEP, and SL-GEP/JADE algorithms. Table IX reports the Suc and RMSE of the algorithms considered for comparison. To assess the performances of multiple algorithms on multiple problems, we first applied the Friedman test to detect whether significant differences exist among all the mean RMSE values obtained by the algorithms, as considered in [47]. Table X presents the results of the Friedman tests for α=0.05. The statistical Friedman value is 59.9451, which is greater than the critical value of 11.07. This indicates a significant difference among the observed results obtained by the algorithms with a probability error of p<0.05. Next, we also adopted the Bonferroni–Dunn’s test as a post-hoc test to detect the significant differences for the control algorithm SL-GEP. The critical difference (CD) value of the Bonferroni–Dunn’s test at α=0.05 is 1.484. Fig. 7 plots the ranking obtained via the Friedman test and the threshold of the CDs of Bonferroni–Dunn’s procedure. The threshold value is equal to the CD value plus the ranking of SL-GEP (i.e., 1.484 + 1.8333 = 3.3173). An algorithm with a ranking larger than the threshold value is considered significantly worse than SL-GEP.

ZHONG et al.: SL-GEP 75
TABLE IX
COMPARE AND CONTRAST THE RESULTS OF GP, GEP-ADF, TREEDE, LDEP, SL-GEP/JADE, AND SL-GEP

TABLE X
RANKING OF GP, GEP-ADF, TREEDE, LDEP, SL-GEP/JADE, AND SL-GEP ACCORDING TO THE STATISTICAL TEST OF THE FRIEDMAN TEST

It can be observed that SL-GEP performed significantly better than GP, GEP-ADF, TreeDE, and LDEP, in terms of the RMSE. Meanwhile, as the ranking of SL-GEP is smaller than the ranking of SL-GEP/JADE plus the CD, the performances of SL-GEP and SL-GEP/JADE are deemed as competitive. The last three rows of Table IX summarize the results of the Wilcoxon’s sign rank test on each problem. It is worth noting that the proposed SL-GEP exhibited significantly better performance.
###SL-GEP ###GEP-ADF2 ###RMSE ###Wilcoxon’s ###test ###Friedman ###test
&&&&
THE STATISTICAL TEST OF THE FRIEDMAN TEST

It can be observed that SL-GEP performed significantly better than GP, GEP-ADF, TreeDE, and LDEP, in terms of the RMSE. Meanwhile, as the ranking of SL-GEP is smaller than the ranking of SL-GEP/JADE plus the CD, the performances of SL-GEP and SL-GEP/JADE are deemed as competitive.

The last three rows of Table IX summarize the results of the Wilcoxon’s sign rank test on each problem. It is worth noting that the proposed SL-GEP exhibited significantly better performance than GP, GEP-ADF, TreeDE, and LDEP on most of the problems, while the performances of SL-GEP and SL-GEP/JADE are competitive. Further, a multiple-problem Wilcoxon’s test is conducted to check the behaviors of the six algorithms on the whole test suite. The statistical results in Table XI indicate that the SL-GEP exhibited significantly better performance than GP, GEP-ADF, TreeDE, and LDEP, while the performances of SL-GEP and SL-GEP/JADE are not significantly different at α=0.05, in terms of the RMSE.

Fig. 7. Bonferroni–Dunn graphic for testing accuracies of GP, GEP-ADF, TreeDE, LDEP, SL-GEP/JADE, and SL-GEP.

In addition, with respect to the Suc values, SL-GEP outperformed GP, GEP-ADF, TreeDE and LDEP on most of the problems. Particularly, for the six even-parity problems, even though the GP, GEP-ADF, TreeDE, and LDEP algorithms achieved a 100% success rate on the three-parity problem, their Suc values is observed to decrease dramatically as the dimensionality of the problem increases. The GEP-ADF, TreeDE, and LDEP are noted to have failed in solving the five-, six-, seven-, and eight-parity problems. Meanwhile, SL-GEP consistently achieved a 100% success rate on the even-parity problems. In summary, SL-GEP exhibits improved performance over GP, GEP-ADF, TreeDE and LDEP in terms of the Suc metric.

76 IEEE TRANSACTIONS ON EVOLUTIONARY COMPUTATION, VOL. 20, NO. 1, FEBRUARY 2016

TABLE XI
RESULTS OF THE MULTIPLE-PROBLEM WILCOXON’S TEST FOR GP, GEP-ADF, TREEDE, LDEP, SL-GEP/JADE, AND SL-GEP

TABLE XII
RT RESULTS OF GP, GEP, GEP-ADF, TREEDE, LDEP, GEP-ADF2, SL-GEP/JADE, AND SL-GEP

E. Analysis of Convergence Speed

This section investigates the convergence speeds of the algorithms under consideration. First of all, we analyze the RT values of all algorithms under-studied to evaluate their efficiencies. As listed in Table XII, the proposed SL-GEP is observed to have outperformed all algorithms except SL-GEP/JADE on most of the problems, in terms of the RT values. As GEP-ADF2 did not use the proposed DE-based search mechanism, it was outperformed by SL-GEP on all 18 problems. This indicates the better efficiency of the proposed DE-based operators versus the original genetic-based operators. Meanwhile, the SL-GEP/JADE outperformed SL-GEP on most of the problems in terms of the RT. This demonstrates that the proposed SL-GEP can be integrated with other forms of state-of-the-art DE to further improve the search performance.
###SL-GEP ###GEP-ADF ###TreeDE ###LDEP ###Wilcoxon's ###test
&&&&
ems, in terms of the RT values. As GEP-ADF2 did not use the proposed DE-based search mechanism, it was outperformed by SL-GEP on all 18 problems. This indicates the better efficiency of the proposed DE-based operators versus the original genetic-based operators. Meanwhile, the SL-GEP/JADE outperformed SL-GEP on most of the problems in terms of the RT. This demonstrates that the proposed SL-GEP can be integrated with other forms of state-of-the-art DE to further improve the search performance.

Further, we compare the RT results of the proposed SL-GEP in Table XII with the published results of ECGP [48]. In [48], the ECGP was applied to five even-parity problems, i.e., four-parity to eight-parity problems. The RT values of ECGP (SL-GEP) on the five problems are 65 296 (36 001), 181 920 (64 224), 287 764 (94 542), 311 940 (158 146), and 540 224 (254 855), respectively. It is clear that the proposed SL-GEP has a much faster convergence speed than ECGP, because the RT values of ECGP are almost two times as large as those of the proposed SL-GEP.

Next, we investigate the impacts of problem dimension on the performances of the algorithms. Fig. 9 shows the RT versus the dimensionality of the even-parity problem. The published results of ECGP are also plotted for comparison analysis. It can be observed that the RT of GP, GEP, GEP-ADF, TreeDE, and LDEP increased dramatically as the dimensionality of the even-parity problem increases, while our proposed GEP-ADF2, SL-GEP, and SL-GEP/JADE exhibited a much lower rate of increase. The proposed algorithms showcased better RT values than the ECGP as the dimensionality of the even-parity problem increases. The results thus indicate that the proposed algorithms exhibited higher scalabilities than the other counterpart algorithms.

Fig. 8 depicts the search convergence trends of the best fitness values attained by the algorithms on six representative problems: 1) F1; 2) F5; 3) F10; 4) F15; 5) three-parity problem; and 6) eight-parity problem. In the plots, note that a search trace terminates when the global optima is reached. It can be observed that the proposed SL-GEP displayed a much faster convergence rate to the global optima or high-quality solutions than the GEP, GEP-ADF, TreeDE, and LDEP. The GP also showcased very fast convergence speed (e.g., F10), but it often quickly gets trapped in local optima.

F. Examples of Converged Solutions
This section showcases some of the converged solutions found by the proposed SL-GEP algorithm. Our objective is to analyze the conciseness and readability of the converged solutions. Table VI reports the structural complexity of the ZHONG et al.: SL-GEP 77.

Fig. 8. Evolution of the best fitness values derived from all compared algorithms on (a) F1, (b) F5, (c) F10, (d) F15, (e) three-parity problem, and (f) eight-parity problem.

Fig. 9. RT versus the dimension of even-parity problem. (For GP, GEP, GEP-ADF, TreeDE, and LDEP, their RT values on large-scale problems are
###SL-GEP ###RT值 ###收敛速度 ###DE-based ###Even-parity
&&&&
ed SL-GEP algorithm. Our objective is to analyze the conciseness and readability of the converged solutions. Table VI reports the structural complexity of the ZHONG et al.: SL-GEP 77 Fig. 8. Evolution of the best fitness values derived from all compared algorithms on (a) F1, (b) F5, (c) F10, (d) F15, (e) three-parity problem, and (f) eight-parity problem. Fig. 9. RT versus the dimension of even-parity problem. (For GP, GEP, GEP-ADF, TreeDE, and LDEP, their RT values on large-scale problems are missing because they failed to locate a global optimal solution in the 100 runs with Emax = 1 000 000. The results of ECGP are cited from [48]). converged solutions on F5, F10, the three-parity problem, and the eight-parity problem. Each of these solutions achieved a perfect hit. If an algorithm failed to locate a solution with a perfect hit across the 100 independent runs, the corresponding value is marked by “N/A” in the table. To quantify the complexities of the converged solutions, the complexity metric proposed in [49] is adopted. This metric determines the structural complexity of an expression based on the total number of nodes in all subtrees. Fig. 10 illustrates an example to determine the complexity of an ET. This measure favors trees with fewer layers and nodes, and is shown as effective for defining Fig. 10. Example of calculating the structure complexity of an expression. the structural complexity of an expression [40], [49]. In our experimental studies, the structural complexity of a solution is equal to the sum of the structural complexity of the main program and those of the ADFs. Since the solutions found by LDEP comprise of a number of low-level instructions, its solutions are omitted from Table XIII. It can be observed that the solutions provided by the SL-GEP were generally more readable, because of their lower structure complexities in most cases. Specifically, on the first symbolic regression problem, the SL-GEP outperformed the GP, GEP, GEP-ADF, and TreeDE. As for the second symbolic problem, the GP, GEP, and GEP-ADF performed slightly better than the SL-GEP, because the expression of this problem can be expressed concisely without using ADFs. On the three-parity problem, SL-GEP significantly outperformed GP, GEP, GEP-ADF, and TreeDE, because the structural complexity of its solution was much smaller than those of the other four algorithms. On the eight-parity problem which is much more complex than the three-parity problem, the GP, GEP, GEP-ADF, and TreeDE all failed to find a global optimal solution in their search. Nevertheless, the SL-DEP was capable of 78 IEEE TRANSACTIONS ON EVOLUTIONARY COMPUTATION, VOL. 20, NO. 1, FEBRUARY 2016 TABLE XIII EXAMPLES OF THE BEST SOLUTIONS FOUND BY GP, GEP, GEP-ADF, TREEDE, AND SL-GEP converging to a global optimal solution on the eight-parity problem. Besides, the solution provided by SL-GEP on the eight-parity problem had a relatively small structural complex-
###SL-GEP ###结构复杂性 ###八位奇偶校验问题 ###算法性能 ###解决方案可读性
&&&&
parity problem, the GP, GEP, GEP-ADF, and TreeDE all failed to find a global optimal solution in their search. Nevertheless, the SL-GEP was capable of converging to a global optimal solution on the eight-parity problem. Besides, the solution provided by SL-GEP on the eight-parity problem had a relatively small structural complexity, which is similar to that of the solution found by GEP-ADF on the three-parity problem.

**78 IEEE TRANSACTIONS ON EVOLUTIONARY COMPUTATION, VOL. 20, NO. 1, FEBRUARY 2016**

**TABLE XIII**
**EXAMPLES OF THE BEST SOLUTIONS FOUND BY GP, GEP, GEP-ADF, TREEDE, AND SL-GEP**

G. Analysis of Algorithm Parameters
The SL-GEP involves four important parameters which are NP, h, h/prime, and K. In this section, we study their impacts by studying SL-GEP with different parameter settings on three representative symbolic regression problems, i.e., F1, F6, and F11. F1 and F6, respectively, represent a kind of simple and a kind of complex symbolic regression problems whose solutions can be compressed effectively with ADFs, while F11 represents another kind of symbolic regression problems whose solutions can be expressed concisely without using ADFs.

1) Impact of NP: First, we study the impact of NP. We varied the value of NP to be 20, 50, 100, 400, and 1000, respectively, while the other parameters remained the same as in Table V. For each parameter setting, 100 independent runs were performed. The results presented in Table XIV show that NP should not be set too small or too large. If NP is set too small, the algorithm may easily get trapped in local optima due to the loss of population diversity. For example, the Suc of SL-GEP on F6 decreased when NP decreased to 20. Meanwhile, a large NP will slow down the search speed. For the three test instances, SL-GEP generally required larger computational cost as NP increased from 50 to 1000. It appears that NP=50 and NP=100 are promising settings.

**TABLE XIV**
**IMPACT OF NP**

**TABLE XV**
**IMPACT OF h**

2) Impact of h: Generally speaking, a larger h enables the main program to represent more complex tree structures, but this will also result in a larger search space. To assess the impact of h, we varied the value of h to be 3, 5, 10, 20, and 40, respectively, while other parameters were set the same as in Table V. The results presented in Table XV show that h should not be set too small. If h is too small, there will be no solution in the search space. For example, with h=3, the SL-GEP failed to find the optimal solution to F6 on all 100 runs. On the other hand, the search space will enlarge as h increases. Hence, SL-GEP generally requires a larger computational cost as h increases. The results in Table XV demonstrate that the performance of SL-GEP gradually degrades when h increases from 20 to 40.

3) Impact of h/prime: h/prime determines the Head length of ADFs. Generally, an ADF with a larger h/prime can accomplish more complex subtasks, but this will also lead to a larger search space. Here, we set h
###SL-GEP ###参数分析 ###符号回归 ###NP ###h ###--- ###**说明：** ###1. ###**删除无用字符 ###格式错误：** ###* ###移除了文本开头的乱码字符 ###`ﬁnd` ###修正为 ###`find`。 ###* ###移除了文本中 ###`h/prime` ###后面未完成的句子 ###`Here ###we ###set ###h` ###因为它是一个不完整的句子 ###且在原文中被截断。 ###* ###修正了 ###`TABLE ###XIII` ###和 ###`TABLE ###XIV` ###`TABLE ###XV` ###的标题格式 ###使其更清晰。 ###* ###修正了 ###`F1 ###F6 ###and ###F11.F1and ###F6` ###为 ###`F1 ###F6 ###and ###F11. ###F1 ###and ###F6` ###增加了空格 ###使其更易读。 ###* ###修正了 ###`NP.W ###e` ###为 ###`NP. ###We`。 ###* ###修正了 ###`Suc ###of ###SL-GEP ###on ###F ###6` ###为 ###`Suc ###of ###SL-GEP ###on ###F6` ###移除了不必要的空格。 ###* ###修正了 ###`NP=50 ###andNP=100` ###为 ###`NP=50 ###and ###NP=100`。 ###* ###修正了 ###`larger ###henables` ###为 ###`larger ###h ###enables`。 ###2. ###**优化排版：** ###* ###在段落之间增加了空行 ###提高可读性。 ###* ###将表格标题（如 ###`TABLE ###XIII`）独立成行并加粗 ###使其更突出。 ###* ###将期刊信息 ###`78 ###IEEE ###TRANSACTIONS ###ON ###EVOLUTIONARY ###COMPUTATION ###VOL. ###20 ###NO. ###1 ###FEBRUARY ###2016` ###独立成行并加粗 ###作为出版信息。 ###3. ###**除乱码字符和排版问题 ###原封不动保存原文：** ###* ###除了上述修正和优化 ###文本内容保持不变。 ###4. ###**提取3-5个关键词：** ###* ###SL-GEP：文章主要研究的对象。 ###* ###参数分析：文章的核心内容是分析算法参数。 ###* ###符号回归：SL-GEP ###应用的领域之一。 ###* ###NP：一个重要的参数。 ###* ###h：另一个重要的参数。
&&&&
optimal solution to F6 on all 100 runs. On the other hand, the search space will enlarge as h increases. Hence, SL-GEP generally requires a larger computational cost as h increases. The results in Table XV demonstrate that the performance of SL-GEP gradually degrades when h increases from 20 to 40.

3) Impact of h': h' determines the Head length of ADFs. Generally, an ADF with a larger h' can accomplish more complex subtasks, but this will also lead to a larger search space. Here, we set h' to be 1, 2, 3, 5, and 10, respectively, to investigate its impact. The results in Table XVI show that the performance of the algorithm degraded significantly on F1 and F6 as h' decreased to 1. However, as for F11, the value of h' seems to have a small impact on the performance of the algorithm. This is because the expressions of F1 and F6 can be effectively compressed by using ADFs, while that of F11 is already concise enough without using ADFs. If h' = 1, the ADFs in each chromosome are too simple to improve the search efficiently. Meanwhile, as h' increases, the ADFs in each chromosome become less general (i.e., less likely to be a frequent substructure). Thus, the performance of the algorithm degraded on these two problems when h' became too large. In general, h' = 2 and h' = 3 lead to better performance.

4) Impact of K: Parameter K is the number of ADFs in each chromosome. To assess its impact, we varied its value to be 1, 2, 5, 10, and 20, respectively. The results in Table XVII show that K had a small impact on the performance of the algorithm for solving F11, because the expressions of solutions to F11 can be concisely represented without using ADFs. However, the performance of the algorithm on F1 and F6 degraded significantly when K became too small (e.g., K=1) or too large (e.g., larger than 5). It appears that the value of K should be set between 2 and 5.

V. CONCLUSION
In this paper, we have proposed a SL-GEP methodology for automatic generation of computer programs. The proposed SL-GEP features a novel chromosome representation that facilitates the formation of C-ADFs that encompass ADFs and/or any subtree of the main program as input arguments. This feature makes the algorithm more flexible to arrive at sophisticated and constructive C-ADFs that improve the accuracy and efficiency of the search. Further, a novel DE-based search mechanism is proposed to efficiently evolve the chromosomes in the SL-GEP. Experiments on 15 symbolic regression problems and six even-parity problems show that the proposed SL-GEP generally performs better than several state-of-the-art GP variants, in terms of accuracy and search efficiency. Besides, the SL-GEP is able to provide more readable solutions that have smaller structural complexities. There are several interesting future research directions. One
###SL-GEP ###ADFs ###搜索空间 ###性能 ###染色体
&&&&
Further, a novel DE-based search mechanism is proposed to efficiently evolve the chromosomes in the SL-GEP. Experiments on 15 symbolic regression problems and six even-parity problems show that the proposed SL-GEP generally performs better than several state-of-the-art GP variants, in terms of accuracy and search efficiency. Besides, the SL-GEP is able to provide more readable solutions that have smaller structural complexities.

There are several interesting future research directions. One direction is to extend the proposed SL-GEP by considering the structural complexity as another objective during the evolution process. By incorporating multiobjective optimization technique, the extended algorithm can provide multiple alternative solutions which have tradeoffs among the accuracy and the readability. The second direction is to further enhance SL-GEP by adaptively controlling the parameters of SL-GEP, such as the length of chromosome and the number of ADFs in each chromosome. Another promising research topic is to apply the proposed SL-GEP to complex practical applications.

REFERENCES
[1] J. R. Koza, Genetic Programming: On the Programming of Computers by Means of Natural Selection, vol. 1. Cambridge, MA, USA: MIT Press, 1992.
[2] P. G. Espejo, S. Ventura, and F. Herrera, “A survey on the application of genetic programming to classification,” IEEE Trans. Syst., Man, Cybern. C, Appl. Rev., vol. 40, no. 2, pp. 121–144, Mar. 2010.
[3] M. O’Neill and C. Ryan, “Grammatical evolution,” IEEE Trans. Evol. Comput., vol. 5, no. 4, pp. 349–358, Aug. 2001.
[4] J. F. Miller and P. Thomson, “Cartesian genetic programming,” in Genetic Programming. Berlin, Germany: Springer, 2000, pp. 121–132.
[5] C. Ferreira, “Gene expression programming: A new adaptive algorithm for solving problems,” Complex Syst., vol. 13, no. 2, pp. 87–129, 2001.
[6] M. F. Brameier and W. Banzhaf, Linear Genetic Programming. New York, NY, USA: Springer, 2007.
[7] C. Zhou, W. Xiao, T. M. Tirpak, and P. C. Nelson, “Evolving accurate and compact classification rules with gene expression programming,” IEEE Trans. Evol. Comput., vol. 7, no. 6, pp. 519–531, Dec. 2003.
[8] C. Ferreira, Gene Expression Programming. Berlin, Germany: Springer, 2006.
[9] N. Sabar, M. Ayob, G. Kendall, and R. Qu, “The automatic design of hyper-heuristic framework with gene expression programming for combinatorial optimization problems,” IEEE Trans. Evol. Comput. [Online]. Available: http://ieeexplore.ieee.org/xpl/articleDetails.jsp?tp=&arnumber=6805577
[10] N. Sabar, M. Ayob, G. Kendall, and R. Qu, “A dynamic multiarmed bandit-gene expression programming hyper-heuristic for combinatorial optimization problems,” IEEE Trans. Cybern., vol. 45, no. 2, pp. 217–228, Feb. 2015.
[11] J. Zhong, L. Luo, W. Cai, and M. Lees, “Automatic rule identification for agent-based crowd models through gene expression programming,” in Proc. Int. Conf. Auton. Agents Multi-Agent Syst., Saint Paul, MN,
###SL-GEP ###Genetic ###Programming ###Gene ###Expression ###Programming ###Multiobjective ###Optimization ###Search ###Mechanism
&&&&
eeexplore.ieee.org/xpl/articleDetails.jsp?tp=&arnumber=6805577

[10] N. Sabar, M. Ayob, G. Kendall, and R. Qu, “A dynamic multiarmed bandit-gene expression programming hyper-heuristic for combinatorial optimization problems,” IEEE Trans. Cybern., vol. 45, no. 2, pp. 217–228, Feb. 2015.
[11] J. Zhong, L. Luo, W. Cai, and M. Lees, “Automatic rule identification for agent-based crowd models through gene expression programming,” in Proc. Int. Conf. Auton. Agents Multi-Agent Syst., Saint Paul, MN, USA, 2014, pp. 1125–1132.
[12] R. Meuth, M.-H. Lim, Y.-S. Ong, and D. C. Wunsch, II, “A proposition on memes and meta-memes in computing for higher-order learning,” Memet. Comput., vol. 1, no. 2, pp. 85–100, 2009.
[13] X. Chen, Y.-S. Ong, M.-H. Lim, and K. C. Tan, “A multi-facet survey on memetic computation,” IEEE Trans. Evol. Comput., vol. 15, no. 5, pp. 591–607, Oct. 2011.
[14] Y. S. Ong, M. H. Lim, and X. Chen, “Memetic computation: Past, present and future,” IEEE Comput. Intell. Mag., vol. 5, no. 2, pp. 24–31, May 2010.
[15] J. R. Koza, Genetic Programming II: Automatic Discovery of Reusable Programs. Cambridge, MA, USA: MIT Press, 1994.
[16] Y. Kameya, J. Kumagai, and Y. Kurata, “Accelerating genetic programming by frequent subtree mining,” in Proc. 10th Annu. Conf. Genet. Evol. Comput. Conf., Atlanta, GA, USA, 2008, pp. 1203–1210.
[17] M. Iqbal, W. Browne, and M. Zhang, “Reusing building blocks of extracted knowledge to solve complex, large-scale Boolean problems,” IEEE Trans. Evol. Comput., vol. 18, no. 4, pp. 465–480, Aug. 2014.
[18] L. Feng, Y.-S. Ong, I. Tsang, and A.-H. Tan, “An evolutionary search paradigm that learns with past experiences,” in Proc. IEEE Congr. Evol. Comput. (CEC), Brisbane, QLD, Australia, 2012, pp. 1–8.
[19] P. J. Angeline and J. Pollack, “Evolutionary module acquisition,” in Proc. 2nd Annu. Conf. Evol. Program., San Diego, CA, USA, 1993, pp. 154–163.
[20] K. E. Kinnear, Jr., “Alternatives in automatic function definition: A comparison of performance,” Advances in Genetic Programming. Cambridge, MA, USA: MIT Press, 1994, pp. 119–141.
[21] T. Van Belle and D. H. Ackley, “Code factoring and the evolution of evolvability,” in Proc. Genet. Evol. Comput. Conf., vol. 2. New York, NY, USA, 2002, pp. 1383–1390.
[22] J. A. Walker and J. F. Miller, “The automatic acquisition, evolution and reuse of modules in Cartesian genetic programming,” IEEE Trans. Evol. Comput., vol. 12, no. 4, pp. 397–417, Aug. 2008.
80 IEEE TRANSACTIONS ON EVOLUTIONARY COMPUTATION, VOL. 20, NO. 1, FEBRUARY 2016
[23] C. Ferreira, “Automatically defined functions in gene expression programming,” in Genetic Systems Programming. Berlin, Germany: Springer, 2006, pp. 21–56.
[24] R. Storn and K. Price, “Differential evolution—A simple and efficient heuristic for global optimization over continuous spaces,” J. Glob. Optim., vol. 11, no. 4, pp. 341–359, 1997.
[25] M. Schmidt and H. Lipson, “Distilling free-form natural laws from
###基因表达编程 ###遗传编程 ###进化计算 ###模因计算 ###优化问题
&&&&
80 IEEE TRANSACTIONS ON EVOLUTIONARY COMPUTATION, VOL. 20, NO. 1, FEBRUARY 2016
[23] C. Ferreira, “Automatically defined functions in gene expression
programming,” in Genetic Systems Programming. Berlin, Germany:
Springer, 2006, pp. 21–56.
[24] R. Storn and K. Price, “Differential evolution—A simple and efficient heuristic for global optimization over continuous spaces,” J. Glob.
Optim., vol. 11, no. 4, pp. 341–359, 1997.
[25] M. Schmidt and H. Lipson, “Distilling free-form natural laws from
experimental data,” Science, vol. 324, no. 5923, pp. 81–85, 2009.
[26] J. McDermott et al., “Genetic programming needs better benchmarks,”
in Proc. Genet. Evol. Comput. Conf., Philadelphia, PA, USA, 2012,
pp. 791–798.
[27] J. Y.-C. Liu, J.-H. A. Chen, C.-T. Chiu, and J.-C. Hsieh, “An exten-
sion of gene expression programming with hybrid selection,” in Proc.
2nd Int. Conf. Intell. Technol. Eng. Syst. (ICITES), Hong Kong, 2014,
pp. 635–641.
[28] Y. Zhang and J. Xiao, “A new strategy for gene expression programming
and its applications in function mining,” Univ. J. Comput. Sci. Eng.
Technol., vol. 1, no. 2, pp. 122–126, 2010.
[29] Y. Peng, C. Yuan, X. Qin, J. Huang, and Y. Shi, “An improved gene
expression programming approach for symbolic regression problems,” Neurocomputing, vol. 137, pp. 293–301, Aug. 2014.
[30] E. Bautu, A. Bautu, and H. Luchian, “AdaGEP—An adaptive gene
expression programming algorithm,” in Proc. Int. Symp. Symbol.
Numer. Algorithms Sci. Comput. (SYNASC), Timisoara, Romania, 2007,
pp. 403–406.
[31] J. Zhang and A. C. Sanderson, “JADE: Adaptive differential evolution
with optional external archive,” IEEE Trans. Evol. Comput., vol. 13,
no. 5, pp. 945–958, Oct. 2009.
[32] Y. Wang, Z. Cai, and Q. Zhang, “Differential evolution with composite
trial vector generation strategies and control parameters,” IEEE Trans.
Evol. Comput., vol. 15, no. 1, pp. 55–66, Feb. 2011.
[33] A. K. Qin and P. N. Suganthan, “Self-adaptive differential evolution
algorithm for numerical optimization,” in Proc. IEEE Congr. Evol.
Comput., vol. 2. Edinburgh, U.K., 2005, pp. 1785–1791.
[34] L. Tang, Y. Dong, and J. Liu, “Differential evolution
with an individual-dependent mechanism,” IEEE Trans.
Evol. Comput. [Online]. Available: http://ieeexplore.ieee.org/
xpl/articleDetails.jsp?tp=&arnumber=6913512
[35] A. Lipowski and D. Lipowska, “Roulette-wheel selection via stochas-
tic acceptance,” Phys. A, Statist. Mech. Appl., vol. 391, no. 6,
pp. 2193–2196, 2012.
[36] C. Ferreira, “Function finding and the creation of numerical constants
in gene expression programming,” in Advances in Soft Computing.
London, U.K.: Springer, 2003, pp. 257–265.
[37] M. Zhang and W. Smart, “Genetic programming with gradient descent
search for multiclass object classification,” in Genetic Programming.
Berlin, Germany: Springer, 2004, pp. 399–408.
[38] M. Kommenda, G. Kronberger, S. Winkler, M. Affenzeller, and
###Gene ###Expression ###Programming ###Differential ###Evolution ###Evolutionary ###Computation ###Genetic ###Programming ###Optimization
&&&&
A, Statist. Mech. Appl., vol. 391, no. 6, pp. 2193–2196, 2012.
[36] C. Ferreira, “Function finding and the creation of numerical constants in gene expression programming,” in Advances in Soft Computing. London, U.K.: Springer, 2003, pp. 257–265.
[37] M. Zhang and W. Smart, “Genetic programming with gradient descent search for multiclass object classification,” in Genetic Programming. Berlin, Germany: Springer, 2004, pp. 399–408.
[38] M. Kommenda, G. Kronberger, S. Winkler, M. Affenzeller, and S. Wagner, “Effects of constant optimization by nonlinear least-squares minimization in symbolic regression,” in Proc. 15th Annu. Conf. Companion Genet. Evol. Comput. Conf. Companion, Amsterdam, The Netherlands, 2013, pp. 1121–1128.
[39] S. Mukherjee and M. J. Eppstein, “Differential evolution of constants in genetic programming improves efficacy and bloat,” in Proc. 14th Int. Conf. Genet. Evol. Comput. Conf. Companion, Philadelphia, PA, USA, 2012, pp. 625–626.
[40] E. J. Vladislavleva, G. F. Smits, and D. den Hertog, “Order of nonlinearity as a complexity measure for models generated by symbolic regression via Pareto genetic programming,” IEEE Trans. Evol. Comput., vol. 13, no. 2, pp. 333–349, Apr. 2009.
[41] S. Luke, The ECJ Owner’s Manual, ECJ Evol. Comput. Libr., San Francisco, CA, USA, 2010.
[42] C. Fonlupt, D. Robilliard, and V. Marion-Poty, “Linear imperative programming with differential evolution,” in Proc. IEEE Symp. Differ. Evol., Paris, France, 2011, pp. 1–8.
[43] C. B. Veenhuis, “Tree based differential evolution,” in Genetic Programming. Berlin, Germany: Springer, 2009, pp. 208–219.
[44] S. Nguyen, M. Zhang, M. Johnston, and K. C. Tan, “A computational study of representations in genetic programming to evolve dispatching rules for the job shop scheduling problem,” IEEE Trans. Evol. Comput., vol. 17, no. 5, pp. 621–639, Oct. 2013.
[45] D. F. Barrero, “Reliability of performance measures in tree-based genetic programming: A study on Koza’s computational effort,” Ph.D. dissertation, School Comput., Univ. Alcalá, Alcalá de Henares, Spain, 2011.
[46] N. Hansen, A. Auger, R. Ros, S. Finck, and P. Pošík, “Comparing results of 31 algorithms from the black-box optimization benchmarking BBOB-2009,” in Proc. Genet. Evol. Comput. Conf., Portland, OR, USA, 2010, pp. 1689–1696.
[47] S. García, A. Fernández, J. Luengo, and F. Herrera, “A study of statistical techniques and performance measures for genetics-based machine learning: Accuracy and interpretability,” Soft Comput., vol. 13, no. 10, pp. 959–977, 2009.
[48] J. A. Walker and J. F. Miller, “Evolution and acquisition of modules in Cartesian genetic programming,” in Genetic Programming. Berlin, Germany: Springer, 2004, pp. 187–197.
[49] G. F. Smits and M. Kotanchek, “Pareto-front exploitation in symbolic regression,” in Genetic Programming Theory and Practice II. New York, NY, USA: Springer, 2005, pp. 283–299.
[50] Z. Huang, “Schema theory for gene expression programming,” Ph.D.
###Genetic ###Programming ###Differential ###Evolution ###Symbolic ###Regression ###Evolutionary ###Computation ###Machine ###Learning
&&&&
tability,” Soft Comput., vol. 13, no. 10, pp. 959–977, 2009.
[48] J. A. Walker and J. F. Miller, “Evolution and acquisition of modules in Cartesian genetic programming,” in Genetic Programming. Berlin, Germany: Springer, 2004, pp. 187–197.
[49] G. F. Smits and M. Kotanchek, “Pareto-front exploitation in symbolic regression,” in Genetic Programming Theory and Practice II. New York, NY, USA: Springer, 2005, pp. 283–299.
[50] Z. Huang, “Schema theory for gene expression programming,” Ph.D. dissertation, School of Engineering and Design, Brunel Univ., Uxbridge, U.K., 2014.

Jinghui Zhong received the B.Eng., M.Eng, and Ph.D. degrees from the School of Information Science and Technology, Sun Yat-sen University, Guangzhou, China, in 2005, 2007, and 2012, respectively.
He is a Research Fellow with the School of Computer Engineering, Nanyang Technological University, Singapore. His research interests include genetic programming, differential evolution, ant colony optimization, and also the applications of evolutionary computations.

Yew-Soon Ong received the B.S. and M.Eng. degrees in electrical and electronics engineering from Nanyang Technological University (NTU), Singapore, in 1998 and 1999, respectively, and the Ph.D. degree in artificial intelligence in complex design from the Computational Engineering and Design Center, University of Southampton, Southampton, U.K., in 2003.
He is currently an Associate Professor and the Director of the A*Star SIMTECH-NTU Joint Laboratory on Complex Systems and Programme, School of Computer Engineering, NTU. He is a Principal Investigator of the Rolls-Royce@NTU Corporate Laboratory on Large Scale Data Analytics, Singapore. His research interests include computational intelligence spans across memetic computation, evolutionary design, machine learning, and big data. His research work on memetic algorithm was featured in the Emerging Research Fronts of the Essential Science Indicators in 2007.
Dr. Ong received the 2015 IEEE Computational Intelligence Magazine Outstanding Paper Award and the 2012 IEEE Transactions on Evolutionary Computation Outstanding Paper Award for his published works on memetic computation. He is the Founding Technical Editor-in-Chief of Memetic Computing Journal; the Founding Chief Editor of Studies in Adaptation, Learning, and Optimization (Springer); and an Associate Editor of IEEE Transactions on Evolutionary Computation, IEEE Transactions on Neural Network and Learning Systems, IEEE Computational Intelligence Magazine, IEEE Transactions on Cybernetics, and IEEE Transactions on Big data.

Wentong Cai received the Ph.D. degree in computer science from University of Exeter, Exeter, U.K., in 1991.
He is a Professor with the School of Computer Engineering, Nanyang Technological University, Singapore, where he is also the Director of the Parallel and Distributed Computing Centre. His research interests include modeling and simulation, particularly, modeling and simulation of large-scale.
###遗传编程 ###进化计算 ###机器学习 ###大数据 ###计算智能
&&&&
National Intelligence Magazine, IEEE Transactions on Cybernetics, and IEEE Transactions on Big Data.
Wentong Cai received the Ph.D. degree in computer science from University of Exeter, Exeter, U.K., in 1991.
He is a Professor with the School of Computer Engineering, Nanyang Technological University, Singapore, where he is also the Director of the Parallel and Distributed Computing Centre. His research interests include modeling and simulation, particularly, modeling and simulation of large-scale complex systems, and system support for distributed simulation and virtual environments, and parallel and distributed computing, particularly, cloud, grid, and cluster computing.
He is an Associate Editor of ACM Transactions on Modeling and Computer Simulation and an Editor of Future Generation Computer Systems.
###Wentong ###Cai ###计算机科学 ###并行分布式计算 ###建模与仿真 ###期刊编辑