Gene expression programming (GEP) is, like genetic algorithms (GAs) and genetic programming (GP), a genetic algorithm as it uses populations of individuals, selects them according to fitness, and introduces genetic variation using one or more genetic operators [1]. The fundamental difference between the three algorithms resides in the nature of the individuals: in GAs the individuals are linear strings of fixed length (chromosomes); in GP the individuals are nonlinear entities of different sizes and shapes (parse trees); and in GEP the individuals are encoded as linear strings of fixed length (the genome or chromosomes) which are afterwards expressed as nonlinear entities of different sizes and shapes (i.e., simple diagram representations or expression trees).

If we have in mind the history of life on Earth (e.g., [2]), we can see that the difference between GAs and GP is only superficial: both systems use only one kind of entity which functions both as genome and body (phenome). These kinds of systems are condemned to have one of two limitations: if they are easy to manipulate genetically, they lose in functional complexity (the case of GAs); if they exhibit a certain amount of functional complexity, they are extremely difficult to reproduce with modification (the case of GP).

Gene Expression Programming: A New Adaptive Algorithm for Solving Problems
Cândida Ferreira†
Departamento de Ciências Agrárias
Universidade dos Açores
9701-851 Terra-Chã
Angra do Heroísmo, Portugal

Gene expression programming, a genotype/phenotype genetic algorithm (linear and ramified), is presented here for the first time as a new technique for the creation of computer programs. Gene expression programming uses character linear chromosomes composed of genes structurally organized in a head and a tail. The chromosomes function as a genome and are subjected to modification by means of mutation, transposition, root transposition, gene transposition, gene recombination, and one- and two-point recombination. The chromosomes encode expression trees which are the object of selection. The creation of these separate entities (genome and expression tree) with distinct functions allows the algorithm to perform with high efficiency that greatly surpasses existing adaptive techniques. The suite of problems chosen to illustrate the power and versatility of gene expression programming includes symbolic regression, sequence induction with and without constant creation, block stacking, cellular automata rules for the density-classification problem, and two problems of boolean concept learning: the 11-multiplexer and the GP rule problem.

In his book, River Out of Eden [3], R. Dawkins gives a list of thresholds of any life explosion. The first is the replicator threshold which consists of a self-copying system in which
###基因表达编程 (GEP) ###遗传算法 (GAs) ###遗传编程 (GP) ###染色体 ###基因组 ###表达树 ###适应性算法 ###计算机程序 ###符号回归 ###序列归纳 ###细胞自动机 ###布尔概念学习 ###Angra do Heroísmo ###Portugal
&&&&
amount of functional complexity, they are extremely difficult to reproduce with modification (the case of GP).
In his book, River Out of Eden [3], R. Dawkins gives a list of thresholds of any life explosion. The first is the replicator threshold which consists of a self-copying system in which there is hereditary variation. Also important is that replicators survive by virtue of their own properties. The second threshold is the phenotype threshold in which replicators survive by virtue of causal effects on something else - the phenotype. A simple example of a replicator/phenotype system is the DNA/protein system of life on Earth. For life to move beyond a very rudimentary stage, the phenotype threshold should be crossed [2, 3].
Similarly, the entities of both GAs and GP (simple replicators) survive by virtue of their own properties. Understandingly, there has been an effort in recent years by the scientific community to cross the phenotype threshold in evolutionary computation. The most prominent effort is developmental genetic programming (DGP) [4] where binary strings are used to encode mathematical expressions. The expressions are decoded using a five-bit binary code, called genetic code. Contrary to its analogous natural genetic code, this “genetic code”, when applied to binary strings, frequently produces invalid expressions (in nature there is no such thing as an invalid protein). Therefore a huge amount of computational resources goes toward editing these illegal structures, which limits this system considerably. Not surprisingly, the gain in performance of DGP over GP is minimal [4, 5].
The interplay of chromosomes (replicators) and expression trees (phenotype) in GEP implies an unequivocal translation system for translating the language of chromosomes into.
###经营模式: 复制器系统 ###表现型系统 ###基因表达编程 (GEP) ###发育遗传编程 (DGP)
产业类型: 生物技术 ###计算机科学 ###人工智能
技术应用: 遗传算法 (GAs) ###遗传编程 (GP) ###二进制编码 ###基因编码
政策措施: 无
专业术语: 复制器阈值 ###表现型阈值 ###遗传变异 ###染色体 ###表达树
地理标识: Bristol BS13 8NU ###UK (英国布里斯托)
&&&&
Figure 1. The flowchart of a gene expression algorithm. The interplay of chromosomes (replicators) and expression trees (phenotype) in GEP implies an unequivocal translation system for translating the language of chromosomes into the language of expression trees (ETs). The structural organization of GEP chromosomes presented in this work allows a truly functional genotype/phenotype relationship, as any modification made in the genome always results in syntactically correct ETs or programs. Indeed, the varied set of genetic operators developed to introduce genetic diversity in GEP populations always produces valid ETs. Thus, GEP is an artificial life system, well established beyond the replicator threshold, capable of adaptation and evolution.

The advantages of a system like GEP are clear from nature, but the most important should be emphasized. First, the chromosomes are simple entities: linear, compact, relatively small, easy to manipulate genetically (replicate, mutate, recombine, transpose, etc.). Second, the ETs are exclusively the expression of their respective chromosomes; they are the entities upon which selection acts and, according to fitness, they are selected to reproduce with modification. During reproduction it is the chromosomes of the individuals, not the ETs, which are reproduced with modification and transmitted to the next generation.

On account of these characteristics, GEP is extremely versatile and greatly surpasses the existing evolutionary techniques. Indeed, in the most complex problem presented in this work, the evolution of cellular automata rules for the density-classification task, GEP surpasses GP by more than four orders of magnitude.

The present work shows the structural and functional organization of GEP chromosomes; how the language of the chromosomes is translated into the language of the ETs; how the chromosomes function as genotype and the ETs as phenotype; and how an individual program is created, matured, and reproduced, leaving offspring with new properties, thus, capable of adaptation. The paper proceeds with a detailed description of GEP and the illustration of this technique with six examples chosen from different fields.

2. An overview of gene expression algorithms
###基因表达算法 ###GEP ###染色体 ###表达树 ###基因型 ###表型 ###遗传操作符 ###人工生命系统 ###进化技术 ###细胞自动机
&&&&
nal organization of GEP chromosomes; how the language of the chromosomes is translated into the language of the ETs; how the chromosomes function as genotype and the ETs as phenotype; and how an individual program is created, matured, and reproduced, leaving offspring with new properties, thus, capable of adaptation. The paper proceeds with a detailed description of GEP and the illustration of this technique with six examples chosen from different fields.

2. An overview of gene expression algorithms
The flowchart of a gene expression algorithm (GEA) is shown in Figure 1. The process begins with the random generation of the chromosomes of the initial population. Then the chromosomes are expressed and the fitness of each individual is evaluated. The individuals are then selected according to fitness to reproduce with modification, leaving progeny with new traits. The individuals of this new generation are, in their turn, subjected to the same developmental process: expression of the genomes, confrontation of the selection environment, and reproduction with modification. The process is repeated for a certain number of generations or until a solution has been found.
Note that reproduction includes not only replication but also the action of genetic operators capable of creating genetic diversity. During replication, the genome is copied and transmitted to the next generation. Obviously, replication alone cannot introduce variation: only with the action of the remaining operators is genetic variation introduced into the population. These operators randomly select the chromosomes to be modified. Thus, in GEP, a chromosome might be modified by one or several operators at a time or not be modified at all. The details of the implementation of GEP operators are shown in section 5.

3. The genome of gene expression programming individuals
In GEP, the genome or chromosome consists of a linear, symbolic string of fixed length composed of one or more genes. It will be shown that despite their fixed length, GEP chromosomes can code ETs with different sizes and shapes.

3.1. Open reading frames and genes
The structural organization of GEP genes is better understood in terms of open reading frames (ORFs). In biology, an ORF, or coding sequence of a gene, begins with the “start” codon, continues with the amino acid codons, and ends at a termination codon. However, a gene is more than the respective ORF, with sequences upstream from the start codon and sequences downstream from the stop codon. Although in GEP the start site is always the first position of a gene, the termination point does not always coincide with the last position of a gene. It is common for GEP genes to have noncoding regions downstream from the termination point. (For now we will not consider these noncoding regions, because they do not interfere with the product of expression.)
Consider, for example, the algebraic expression:
, (3.1)
###基因表达编程 (GEP) ###基因表达算法 (GEA) ###染色体 ###基因组 ###基因 ###开放阅读框 (ORF) ###遗传操作符 ###复制 ###适应性 ###遗传多样性
&&&&
tart codon and sequences downstream from the stop codon. Although in GEP the start site is always the first position of a gene, the termination point does not always coincide with the last position of a gene. It is common for GEP genes to have noncoding regions downstream from the termination point. (For now we will not consider these noncoding regions, because they do not interfere with the product of expression.)

Consider, for example, the algebraic expression:
, (3.1)
which can also be represented as a diagram or ET: Looking only at the structure of GEP ORFs, it is difficult or even impossible to see the advantages of such a representation, except perhaps for its simplicity and elegance. However, when ORFs are analyzed in the context of a gene, the advantages of such representation become obvious. As stated previously, GEP chromosomes have fixed length and are composed of one or more genes of equal length. Therefore the length of a gene is also fixed. Thus, in GEP, what varies is not the length of genes (which is constant), but the length of the ORFs. Indeed, the length of an ORF may be equal to or less than the length of the gene. In the first case, the termination point coincides with the end of the gene, and in the second case, the termination point is somewhere upstream from the end of the gene.

So, what is the function of these noncoding regions in GEP genes? They are, in fact, the essence of GEP and evolvability, for they allow modification of the genome using any genetic operator without restrictions, always producing syntactically correct programs without the need for a complicated editing process or highly constrained ways of implementing genetic operators. Indeed, this is the paramount difference between GEP and previous GP implementations, with or without linear genomes (for a review on GP with linear genomes see [7]).

3.2. Gene expression programming genes
GEP genes are composed of a head and a tail. The head contains symbols that represent both functions (elements from the function set F) and terminals (elements from the terminal set T), whereas the tail contains only terminals. Therefore two different alphabets occur at different regions within a Q Q* a a a ab The inverse process, that is, the translation of a K-expression into an ET, is also very simple. Consider the following K-expression:
01234567890
Q*+*a*Qaaba (3.3)
The start position (position 0) in the ORF corresponds to the root of the ET. Then, below each function are attached as many branches as there are arguments to that function. The assemblage is complete when a baseline composed only of terminals (the variables or constants used in a problem) is formed. In this case, the following ET is formed:
where “Q” represents the square root function. This kind of diagram representation is in fact the phenotype of GEP individuals, being the genotype easily inferred from the phenotype as follows:
01234567
###基因表达编程 (GEP) ###开放阅读框 (ORF) ###非编码区 ###遗传算子 ###基因组 ###进化能力 ###基因型 ###表型 ###表达式树 (ET) ###K-表达式
&&&&
responds to the root of the ET. Then, below each function are attached as many branches as there are arguments to that function. The assemblage is complete when a baseline composed only of terminals (the variables or constants used in a problem) is formed. In this case, the following ET is formed:
where “Q” represents the square root function. This kind of diagram representation is in fact the phenotype of GEP individuals, being the genotype easily inferred from the phenotype as follows:
Q*+-abcd (3.2)
which is the straightforward reading of the ET from left to right and from top to bottom. Expression (3.2) is an ORF, starting at “Q” (position 0) and terminating at “d” (position 7). These ORFs were named K-expressions (from the Karva language, the name I chose for the language of GEP). Note that this ordering differs from both the postfix and prefix expressions used in different GP implementations with arrays or stacks [6].
For each problem, the length of the head h is chosen, whereas the length of the tail t is a function of h and the number of arguments of the function with the most arguments n, and is evaluated by the equation:
t = h (n-1) + 1. (3.4)
Consider a gene composed of {Q, *, /, -, +, a, b}. In this case n = 2. For instance, for h = 10 and t = 11, the length of the gene is 10+11=21. One such gene is shown below (the tail is shown in bold):
+Q-/b*aaQbaabaabbaaab (3.5)
and it codes for the following ET:
In this case, the ORF ends at position 10, whereas the gene ends at position 20.
Suppose now a mutation occurred at position 9, changing the “b” into “+”. Then the following gene is obtained:
+Q-/b*aaQ+aabaabbaaab (3.6)
and its ET gives:
+Q-/b*+*Qbaabaabbaaab (3.7)
giving the ET:
In this case the termination point shifts several positions to the right (position 14).
Obviously the opposite also happens, and the ORF is shortened. For example, consider gene (3.5) and suppose a mutation occurred at position 5, changing the “*” into “a”:
+Q-/baaaQbaabaabbaaab (3.8)
Its expression results in the following ET:
In this case, the ORF ends at position 7, shortening the original ET by 3 nodes.
Despite its fixed length, each gene has the potential to code for ETs of different sizes and shapes, the simplest being composed of only one node (when the first element of a gene is a terminal) and the biggest composed of as many nodes as the length of the gene (when all the elements of the head are functions with the maximum number of arguments, n).
It is evident from the examples above, that any modifica-
###ET ###GEP ###K-expressions ###Karva language ###Gene ###ORF ###Mutation ###Phenotype ###Genotype ###Terminal ###Function ###Argument
&&&&
In this case, the ORF ends at position 7, shortening the original ET by 3 nodes. Despite its fixed length, each gene has the potential to code for ETs of different sizes and shapes, the simplest being composed of only one node (when the first element of a gene is a terminal) and the biggest composed of as many nodes as the length of the gene (when all the elements of the head are functions with the maximum number of arguments, n). It is evident from the examples above, that any modification made in the genome, no matter how profound, always results in a valid ET. Obviously the structural organization of genes must be preserved, always maintaining the boundaries between head and tail and not allowing symbols from the function set on the tail. Section 5 shows how GEP operators work and how they modify the genome of GEP individuals during reproduction. In this case, the termination point shifts two positions to the right (position 12).

Suppose now that a more radical modification occurred, and the symbols at positions 6 and 7 in gene (3.5) change respectively into “+” and “*”, creating the following gene:
b*ab*baQb ab*b-b*b *Qb+ -*Qaabbab abbba bbaba (b)

3.3. Multigenic chromosomes
GEP chromosomes are usually composed of more than one gene of equal length. For each problem or run, the number of genes, as well as the length of the head, is chosen. Each gene codes for a sub-ET and the sub-ETs interact with one another forming a more complex multisubunit ET. The details of such interactions are fully explained in section 3.4.

Consider, for example, the following chromosome with length 27, composed of three genes (the tails are shown in bold):
-b*babbab*Qb+abbba-*Qabbaba (3.9)
It has three ORFs, and each ORF codes for a sub-ET (Figure 2). Position 0 marks the start of each gene; the end of each ORF, though, is only evident upon construction of the respective sub-ET. As shown in Figure 2, the first ORF ends at position 4 (sub-ET1); the second ORF ends at position 5 (sub-ET2); and the last ORF also ends at position 5 (sub-ET3). Thus, GEP chromosomes code for one or more ORFs, each expressing a particular sub-ET. Depending on the task at hand, these sub-ETs may be selected individually according to their respective fitness (e.g., in problems with multiple outputs), or they may form a more complex, multi-subunit ET and be selected according to the fitness of the whole, multi-subunit ET. The patterns of expression and the details of selection will be discussed throughout this paper. However, keep in mind that each sub-ET is both a separate entity and a part of a more complex, hierarchical structure, and, as in all complex systems, the whole is more than the sum of its parts.

3.4. Expression trees and the phenotype
In nature, the phenotype has multiple levels of complexity.
###GEP ###Expression Trees (ETs) ###Genome ###Gene ###Chromosome ###Sub-ET ###ORF ###Phenotype ###Multigenic ###Multi-subunit ET
&&&&
may form a more complex, multi-subunit ET and be selected according to the fitness of the whole, multi-subunit ET. The patterns of expression and the details of selection will be discussed throughout this paper. However, keep in mind that each sub-ET is both a separate entity and a part of a more complex, hierarchical structure, and, as in all complex systems, the whole is more than the sum of its parts.

3.4. Expression trees and the phenotype
In nature, the phenotype has multiple levels of complexity, the most complex being the organism itself. But tRNAs, proteins, ribosomes, cells, and so forth, are also products of expression, and all of them are ultimately encoded in the genome. In all cases, however, the expression of the genetic information starts with transcription (the synthesis of RNA) and, for protein genes, proceeds with translation (the synthesis of proteins).

3.4.1. Information decoding: Translation
In GEP, from the simplest individual to the most complex, the expression of genetic information starts with translation, the transfer of information from a gene into an ET. This process has already been presented in section 3.2 where decoding of GEP genes is shown. In contrast to nature, the expression of the genetic information in GEP is very simple. Worth emphasizing is the fact that in GEP there is no need for transcription: the message in the gene is directly translated into an ET.

GEP chromosomes are composed of one or more ORFs, and obviously the encoded individuals have different degrees of complexity. The simplest individuals are encoded in a single gene, and the “organism” is, in this case, the product of a single gene - an ET. In other cases, the organism is a multi-subunit ET, in which the different sub-ETs are linked together by a particular function. In other cases, the organism emerges from the spatial organization of different sub-ETs (e.g., in planning and problems with multiple outputs). And, in yet other cases, the organism emerges from the interactions of conventional sub-ETs with different domains (e.g., neural networks). However, in all cases, the whole organism is encoded in a linear genome.

Figure 2. Expression of GEP genes as sub-ETs. (a) A three-genic chromosome with the tails shown in bold. The arrows show the termination point of each gene. (b) The sub-ETs codified by each gene.

3.4.2. Interactions of sub-expression trees
We have seen that translation results in the formation of sub-ETs with different complexity, but the complete expression of the genetic information requires the interaction of these sub-ETs with one another. One of the simplest interactions is the linking of sub-ETs by a particular function. This process is similar to the assemblage of different protein subunits into a multi-subunit protein.

When the sub-ETs are algebraic or boolean expressions,
###GEP ###表达树 (ET) ###亚表达树 (sub-ET) ###基因表达 ###翻译 ###基因组 ###染色体 ###开放阅读框 (ORF) ###多亚基ET ###遗传信息解码 ###神经网络 ###蛋白质合成
&&&&
3.4.2. Interactions of sub-expression trees
We have seen that translation results in the formation of sub-ETs with different complexity, but the complete expression of the genetic information requires the interaction of these sub-ETs with one another. One of the simplest interactions is the linking of sub-ETs by a particular function. This process is similar to the assemblage of different protein subunits into a multi-subunit protein.

When the sub-ETs are algebraic or boolean expressions, any mathematical or boolean function with more than one argument can be used to link the sub-ETs into a final, multi-subunit ET. The functions most chosen are addition or multiplication for algebraic sub-ETs, and OR or IF for boolean sub-ETs.

In the current version of GEP the linking function is a priori chosen for each problem, but it can be easily introduced in the genome; for instance, in the last position of chromosomes, and also be subjected to adaptation. Indeed, preliminary results suggest that this system works very well.

Figure 3 illustrates the linking of two sub-ETs by addition. Note that the root of the final ET (+) is not encoded by the genome. Note also that the final ET could be linearly encoded as the following K-expression:
+Q**-bQ+abbba (3.10)

However, to evolve solutions for complex problems, it is more effective to use multigenic chromosomes, for they permit the modular construction of complex, hierarchical structures, where each gene codes for a small building block.

Figure 3. Expression of multigenic chromosomes as ETs. (a) A two-genic chromosome with the tails shown in bold. (b) The sub-ETs codified by each gene. (c) The result of posttranslational linking with addition. These small building blocks are separated from each other, and thus can evolve independently. For instance, if we tried to evolve a solution for the symbolic regression problem presented in section 6.1 with single-gene chromosomes, the success rate would fall significantly (see section 6.1). In that case the discovery of small building blocks is more constrained as they are no longer free to evolve independently. This kind of experiment shows that GEP is in effect a powerful, hierarchical invention system capable of easily evolving simple blocks and using them to form more complex structures [8, 9].

Figure 4 shows another example of sub-ET interaction, where three boolean sub-ETs are linked by the function IF. The multi-subunit ET could be linearized as the following K-expression:
IINAIAINu1ca3aa2acAOab2 (3.11)

Figure 5 shows another example of sub-ET interaction,
###基因表达编程 (GEP) ###子表达式树 (sub-ET) ###多基因染色体 ###遗传信息 ###蛋白质亚基 ###代数表达式 ###布尔表达式 ###K-表达式 ###符号回归 ###分层发明系统
&&&&
实验表明，GEP（Gene Expression Programming）实际上是一个强大的分层发明系统，能够轻松地进化简单的块并使用它们形成更复杂的结构 [8, 9]。

图4展示了子ET（Expression Tree）交互的另一个例子，其中三个布尔子ET通过IF函数连接。多单元ET可以线性化为以下K-表达式：
IINAIAINu1ca3aa2acAOab2 (3.11)

图5展示了子ET交互的另一个例子，其中子ET是最简单的类型（单元素子ET）。在这种情况下，子ET通过IF函数3个一组连接，然后这些簇又通过另一个IF函数3个一组连接，最后三个簇也通过IF连接，形成一个大的多单元ET。这种染色体结构被用于解决第6.5.2节中的11-多路复用器问题，以及进化用于密度分类问题的细胞自动机规则。图5中的个体可以转换为以下K-表达式：
IIIIIIIIIIIII131u3ab2ubab23c3ua31a333au3 (3.12)

最后，某些染色体的完整表达需要顺序执行小计划，其中第一个子ET完成少量工作，第二个从那里继续，依此类推。最终计划是所有子计划有序行动的结果（参见第6.3节中的块堆叠问题）。

连接函数的类型，以及基因的数量和每个基因的长度，都是针对每个问题预先选择的。因此，我们总是可以从使用单基因染色体开始，逐渐增加头部的长度；如果它变得非常大，我们可以增加基因的数量，当然也可以选择一个函数来连接它们。我们可以从加法或OR开始，但在其他情况下，另一个连接函数可能更合适。当然，目的是找到一个好的解决方案，而GEP提供了找到解决方案的方法。

4. 适应度函数和选择

图4. 多基因染色体作为ET的表达。
(a) 带有粗体所示尾部的三基因染色体（“N”是一个参数的函数，表示NOT；“A”和“O”是两个参数的函数，分别表示AND和OR；“I”是三个参数的函数，表示IF；其余符号是终端）。
(b) 每个基因编码的子ET。
(c) 翻译后与IF连接的结果。

图5. 多基因染色体作为ET的表达。
(a) 由单元素基因组成的27基因染色体。
(b) 翻译后与IF连接的结果。
###GEP ###基因表达编程 ###表达式树 ###子ET ###K-表达式 ###多路复用器问题 ###密度分类问题 ###适应度函数 ###染色体结构 ###连接函数 ###细胞自动机 ###布尔函数
&&&&
he length of each gene, are a priori chosen for each problem. So, we can always start by using a single-gene chromosome, gradually increasing the length of the head; if it becomes very large, we can increase the number of genes and of course choose a function to link them. We can start with addition or OR, but in other cases another linking function might be more appropriate. The idea, of course, is to find a good solution, and GEP provides the means of finding one.

4. Fitness functions and selection
In this section, two examples of fitness functions are described. Other examples of fitness functions are given in the problems studied in section 6. The success of a problem greatly depends on the way the fitness function is designed: the goal must be clearly and correctly defined in order to make the system evolve in that direction.

4.1. Fitness functions
One important application of GEP is symbolic regression or function finding (e.g., [9]), where the goal is to find an expression that performs well for all fitness cases within a certain error of the correct value. For some mathematical applications it is useful to use small relative or absolute errors in order to discover a very good solution. But if the range of selection is excessively narrowed, populations evolve very slowly and are incapable of finding a correct solution. On the other hand, if the opposite is done and the range of selection is broadened, numerous solutions will appear with maximum fitness that are far from good solutions.

To solve this problem, an evolutionary strategy was devised that permits the discovery of very good solutions without halting evolution. So, the system is left to find for itself the best possible solution within a minimum error. For that a very broad limit for selection to operate is given, for instance, a relative error of 20%, that allows the evolutionary process to get started. Indeed, these founder individuals are usually very unfit but their modified descendants are reshaped by selection and populations adapt wonderfully, finding better solutions that progressively approach a perfect solution. Mathematically, the fitness fi of an individual program i is expressed by equation (4.1a) if the error chosen is the absolute error, and by equation (4.1b) if the error chosen is the relative error:

(4.1a)
(4.1b)
where M is the range of selection, C(i,j) the value returned by the individual chromosome i for fitness case j (out of Ct fitness cases), and Tj is the target value for fitness case j. Note that for a perfect fit C(i,j) = Tj and fi = fmax = Ct . M. Note that with this kind of fitness function the system can find the optimal solution for itself.

In another important GEP application, boolean concept
###GEP ###Fitness functions ###Symbolic regression ###Evolutionary strategy ###Chromosome ###Selection ###Absolute error ###Relative error ###Optimal solution ###Boolean concept
&&&&
(4.1a)
(4.1b)
其中 M 是选择范围，C(i,j) 是个体染色体 i 对于适应度案例 j（总共 Ct 个适应度案例）返回的值，Tj 是适应度案例 j 的目标值。请注意，对于完美拟合，C(i,j) = Tj 且 fi = fmax = Ct . M。请注意，使用这种适应度函数，系统可以自行找到最优解。

在另一个重要的 GEP 应用中，布尔概念学习或逻辑综合（例如，[9]），个体的适应度是其正确执行的适应度案例数量的函数。然而，对于大多数布尔应用，惩罚能够正确解决大约 50% 适应度案例的个体是至关重要的，因为这很可能只反映了正确解决二进制布尔函数 50% 的可能性。因此，建议只选择能够解决 50% 到 75% 以上适应度案例的个体。低于该标记，可以赋予一个符号适应度值，例如 fi = 1。通常，进化的过程是从这些不适应的个体开始的，因为它们在初始种群中很容易被创建。然而，在未来的世代中，高度适应的个体开始出现，并在种群中迅速传播。对于简单的问题，如具有 2 到 5 个参数的布尔函数，这并不是很重要，但对于更复杂的问题，选择一个底线是方便的。对于这些问题，可以使用以下适应度函数：

(4.2)
其中 n 是正确评估的适应度案例数量，Ct 是适应度案例总数。

4.2. 选择
在本工作中提出的所有问题中，个体都是根据适应度通过轮盘赌抽样 [10] 结合最佳个体克隆（简单精英主义）进行选择的。对不同选择方案（带和不带精英主义的轮盘赌选择、带和不带精英主义的锦标赛选择，以及带和不带精英主义的各种确定性选择）的初步研究表明，只要保证最佳个体的克隆（结果未显示），它们之间没有明显的差异。有些方案在一个问题中表现更好，另一些在另一个问题中表现更好。然而，对于更复杂的问题，似乎带精英主义的轮盘赌选择是最好的。

5. 繁殖与变异
根据适应度和轮盘赌的运气，个体被选择进行繁殖和变异，从而产生必要的遗传多样性，从而实现长期的进化。

除了复制（其中所有选定个体的基因组被严格复制）之外，所有其余的操作符随机选择染色体进行某种修改。然而，除了突变之外，每个个体都是如此。
###GEP应用 ###布尔概念学习 ###逻辑综合 ###适应度函数 ###轮盘赌抽样 ###精英主义 ###遗传多样性 ###进化 ###染色体 ###突变 ###基因组 ###繁殖
&&&&
Except for replication, where the genomes of all the selected individuals are rigorously copied, all the remaining operators randomly pick chromosomes to be subjected to a certain modification. However, except for mutation, each of a neutral mutation, as it occurred in the noncoding region of the gene.

It is worth noticing that in GEP there are no constraints neither in the kind of mutation nor the number of mutations in a chromosome: in all cases the newly created individuals are syntactically correct programs.

In nature, a point mutation in the sequence of a gene can slightly change the structure of the protein or not change it at all, as neutral mutations are fairly frequent (e.g., mutations in introns, mutations that result in the same amino acid due to the redundancy of the genetic code, etc.). Here, although neutral mutations exist (e.g., mutations in the noncoding regions), a mutation in the coding sequence of a gene has a much more profound effect: it usually drastically reshapes the ET.

5.3. Transposition and insertion sequence elements
The transposable elements of GEP are fragments of the genome that can be activated and jump to another place in the chromosome. In GEP there are three kinds of transposable elements. (1) Short fragments with a function or terminal in the first position that transpose to the head of genes, except to the root (insertion sequence elements or IS elements). (2) Short fragments with a function in the first position that transpose to the root of genes (root IS elements or RIS elements). (3) Entire genes that transpose to the beginning of chromosomes.

The existence of IS and RIS elements is a remnant of the developmental process of GEP, as the first GEA used only single-gene chromosomes, and in such systems a gene with a terminal at the root was of little use. When multigenic chromosomes were introduced this feature remained as these operators are important to understand the mechanisms of genetic variation and evolvability.

5.3.1. Transposition of insertion sequence elements
Any sequence in the genome might become an IS element, therefore these elements are randomly selected throughout the chromosome. A copy of the transposon is made and inserted at any position in the head of a gene, except at the start position.

Typically, an IS transposition rate (pis) of 0.1 and a set of three IS elements of different length are used. The transposition operator randomly chooses the chromosome, the start of the IS element, the target site, and the length of the transposon. Consider the 2-genic chromosome below:
012345678901234567890012345678901234567890
*-+*a-+a*bbabbaabababQ**+abQbb*aa bbaaaabba
Suppose that the sequence “bba” in gene 2 (positions 12
###GEP ###基因表达式编程 ###基因组 ###染色体 ###突变 ###转座 ###插入序列元件 (IS elements) ###根插入序列元件 (RIS elements) ###遗传变异 ###可进化性 ###中性突变 ###转座子
&&&&
Typically, an IS transposition rate (p_is) of 0.1 and a set of three IS elements of different length are used. The transposition operator randomly chooses the chromosome, the start of the IS element, the target site, and the length of the transposon. Consider the 2-genic chromosome below:
012345678901234567890012345678901234567890
*-+*a-+a*bbabbaabababQ**+abQbb*aa bbaaaabba
Suppose that the sequence “bba” in gene 2 (positions 12 through 14) was chosen to be an IS element, and the target site was bond 6 in gene 1 (between positions 5 and 6). Then, a cut is made in bond 6 and the block “bba” is copied into the site of insertion, obtaining: operator is not allowed to modify a chromosome more than once. For instance, for a transposition rate of 0.7, seven out of 10 different chromosomes are randomly chosen.

Furthermore, in GEP, a chromosome might be chosen by none or several genetic operators that introduce variation in the population. This feature also distinguishes GEP from GP where an entity is never modified by more than one operator at a time [9]. Thus, in GEP, the modifications of several genetic operators accumulate during reproduction, producing offspring very different from the parents.

We now proceed with the detailed description of GEP operators, starting obviously with replication. (Readers less concerned with implementation details of genetic operators may wish to skip this section.)

5.1. Replication
Although vital, replication is the most uninteresting operator: alone it contributes nothing to genetic diversification. (Indeed, replication, together with selection, is only capable of causing genetic drift.) According to fitness and the luck of the roulette, chromosomes are faithfully copied into the next generation. The fitter the individual the higher the probability of leaving more offspring. Thus, during replication the genomes of the selected individuals are copied as many times as the outcome of the roulette. The roulette is spun as many times as there are individuals in the population, always maintaining the same population size.

5.2. Mutation
Mutations can occur anywhere in the chromosome. However, the structural organization of chromosomes must remain intact. In the heads any symbol can change into another (function or terminal); in the tails terminals can only change into terminals. This way, the structural organization of chromosomes is maintained, and all the new individuals produced by mutation are structurally correct programs.

Typically, a mutation rate (p_m) equivalent to two point mutations per chromosome is used. Consider the following 3-genic chromosome:
012345678012345678012345678
-+-+abaaa/bb/ababb*Q*+aaaba
Suppose a mutation changed the element in position 0 in gene 1 to “Q”; the element in position 3 in gene 2 to “Q”; and the element in position 1 in gene 3 to “b”, obtaining:
012345678012345678012345678
Q+-+abaaa/bbQababb*b*+aaaba
###GEP ###遗传编程 ###染色体 ###基因 ###转座 ###复制 ###突变 ###遗传操作符 ###种群 ###遗传漂变
&&&&
所有通过突变产生的新个体在结构上都是正确的程序。通常，使用相当于每个染色体两个点突变的突变率（pm）。考虑以下3基因染色体：
012345678012345678012345678
-+-+abaaa/bb/ababb*Q*+aaaba
假设突变将基因1中位置0的元素更改为“Q”；将基因2中位置3的元素更改为“Q”；并将基因3中位置1的元素更改为“b”，得到：
012345678012345678012345678
Q+-+abaaa/bbQababb*b*+aaaba
请注意，如果一个函数突变为一个终端或反之，或者一个单参数函数突变为一个双参数函数或反之，则ET会发生剧烈变化。另请注意，基因2上的突变是一个例子。
*-+*a-bba+babbaabababQ**+abQbb*aa bbaaaabba
在转座过程中，插入位点上游的序列保持不变，而复制的IS元件下游的序列在头部末端丢失了与IS元件长度相同的符号（在这种情况下，“a*b”序列被删除）。请注意，尽管有这种插入，染色体的结构组织仍然保持不变，因此所有新创建的个体都是语法正确的程序。另请注意，转座可以极大地重塑ET，插入位点越靠上，变化越深远。因此，这种操作符（IS转座和下面的RIS转座）可能被视为在ET的最低级别具有高命中率[7]。

5.3.2. 根转座
所有RIS元件都以函数开头，因此从头部序列中选择。为此，在头部随机选择一个点，并向下扫描基因直到找到一个函数。该函数成为RIS元件的起始位置。如果没有找到函数，则不执行任何操作。
通常使用0.1的根转座率（pris）和一组不同大小的三个RIS元件。该操作符随机选择染色体、要修改的基因、RIS元件的起始位置及其长度。考虑以下2基因染色体：
-ba*+-+-Q/abababbbaaaQ*b/ +bbabbaaaaaaaabbb
假设基因2中的序列“+bb”被选为RIS元件。然后，将转座子复制到基因的根部，得到：
-ba*+-+-Q/abababbbaaa +bbQ*b/+bbaaaaaaaabbb
在根转座过程中，整个头部会移动以容纳RIS元件，同时丢失头部末端的符号（与转座子长度相同）。与IS元件一样，受转座影响的基因尾部和所有附近的基因保持不变。再次注意，新创建的程序是语法正确的，因为染色体的结构组织保持不变。
根转座引起的修改是...
###突变 ###染色体 ###基因 ###转座 ###IS元件 ###RIS元件 ###根转座 ###程序结构 ###语法正确 ###遗传算法 ###生物信息学 ###基因组编辑
&&&&
During root transposition, the whole head shifts to accommodate the RIS element, losing, at the same time, the last symbols of the head (as many as the transposon length). As with IS elements, the tail of the gene subjected to transposition and all nearby genes stay unchanged. Note, again, that the newly created programs are syntactically correct because the structural organization of the chromosome is maintained.

The modifications caused by root transposition are extremely radical, because the root itself is modified. In nature, if a transposable element is inserted at the beginning of the coding sequence of a gene, causing a frameshift mutation, it radically changes the encoded protein. Like mutation and IS transposition, root insertion has a tremendous transforming power and is excellent for creating genetic variation.

5.3.3. Gene transposition
In gene transposition an entire gene functions as a transposon and transposes itself to the beginning of the chromosome. In contrast to the other forms of transposition, in gene transposition the transposon (the gene) is deleted in the place of origin. This way, the length of the chromosome is maintained.

The chromosome to undergo gene transposition is randomly chosen, and one of its genes (except the first, obviously) is randomly chosen to transpose. Consider the following chromosome composed of 3 genes:
*a-*abbab-QQ/aaabb Q+abababb
Suppose gene 2 was chosen to undergo gene transposition. Then the following chromosome is obtained:
-QQ/aaabb *a-*abbabQ+abababb

Note that for numerical applications where the function chosen to link the genes is addition, the expression evaluated by the chromosome is not modified. But the situation differs in other applications where the linking function is not commutative, for instance, the IF function chosen to link the sub-ETs in the 11-multiplexer problem in section 6.5.2. However, the transforming power of gene transposition reveals itself when this operator is conjugated with crossover. For example, if two functionally identical chromosomes or two chromosomes with an identical gene in different positions recombine, a new individual with a duplicated gene might appear. It is known that the duplication of genes plays an important role in biology and evolution (e.g., [11]). Interestingly, in GEP, individuals with duplicated genes are commonly found in the process of problem solving.

5.4. Recombination
In GEP there are three kinds of recombination: one-point, two-point, and gene recombination. In all cases, two parent chromosomes are randomly chosen and paired to exchange some material between them.

5.4.1. One-point recombination
During one-point recombination, the chromosomes cross over a randomly chosen point to form two daughter chromosomes. Consider the following parent chromosomes:
-b+Qbbabb/aQbbbaab/-a/ababb-ba-abaaa
Suppose bond 3 in gene 1 (between positions 2 and 3) was
###基因转座 ###染色体 ###转座子 ###遗传变异 ###基因复制 ###重组 ###GEP ###根转座 ###IS元素 ###移码突变 ###编码蛋白 ###基因组学
&&&&
GEP（Gene Expression Programming，基因表达式编程）中有三种重组方式：单点重组、两点重组和基因重组。在所有情况下，随机选择并配对两个亲本染色体，以在它们之间交换一些遗传物质。

5.4.1. 单点重组
在单点重组中，染色体在一个随机选择的点上交叉，形成两个子代染色体。考虑以下亲本染色体：
012345678012345678
-b+Qbbabb/aQbbbaab/-a/ababb-ba-abaaa
假设基因1中的键3（位置2和3之间）被随机选为交叉点。然后，配对的染色体在该键处被切开，并在交叉点下游交换物质，形成以下子代：
012345678012345678
-b+/ababb-ba-abaaa
/-aQbbabb/aQbbbaab
通过这种重组，大多数情况下，产生的子代表现出与亲本不同的特性。单点重组，像上述操作符一样，是遗传变异的一个非常重要的来源，在突变之后，它是GEP中最常选择的操作符之一。所使用的单点重组率（p1r）取决于其他操作符的速率。通常使用0.7的全局交叉率（三种重组方式的速率之和）。

5.4.2. 两点重组
在两点重组中，染色体被配对，并随机选择两个重组点。重组点之间的物质随后在两个染色体之间交换，形成两个新的子代染色体。考虑以下亲本染色体：
0123456789001234567890
+*a*bbcccac*baQ*acabab -[1]
*cbb+cccbcc++**bacbaab-[2]
假设基因1中的键7（位置6和7之间）和基因2中的键3（位置2和3之间）被选为交叉点。然后，配对的染色体在这些键处被切开，并交换交叉点之间的物质，形成以下子代：
0123456789001234567890
+*a*bbc cbcc++*Q*acabab -[3]
*cbb+ccccac*ba *bacbaab-[4]
请注意，在两个亲本中，第一个基因都在终止点下游被分割。事实上，GEP染色体的非编码区是染色体可以被分割以进行交叉而不会干扰ORF的理想区域。另请注意，染色体1的第二个基因也在终止点下游被切开。然而，染色体2的基因2在终止点上游被分割，这深刻地改变了子ET。另请注意，当这些染色体重组时，染色体1的基因2的非编码区被激活并整合到染色体3中。
两点重组的转化能力大于单点重组，并且在解决更复杂的问题时最有用，尤其是在使用由多个基因组成的多基因染色体时。

5.4.3. 基因重组
在基因重组中，整个基因在重组过程中被交换。
###GEP ###基因表达式编程 ###染色体 ###重组 ###单点重组 ###两点重组 ###基因重组 ###遗传变异 ###交叉率 ###非编码区 ###多基因染色体 ###遗传算法
&&&&
nation point, profoundly changing the sub-ET. Note also that when these chromosomes recombined, the noncoding region of gene 2 of chromosome 1 was activated and integrated into chromosome 3.
The transforming power of two-point recombination is greater than one-point recombination, and is most useful to evolve solutions for more complex problems, especially when multigenic chromosomes composed of several genes are used.

5.4.3. Gene recombination
In gene recombination an entire gene is exchanged during crossover. The exchanged genes are randomly chosen and occupy the same position in the parent chromosomes. Consider the following parent chromosomes:
012345678012345678012345678
/aa-abaaa/a*bbaaab/Q*+aaaab/-*/abbabQ+aQbabaa-Q/Qbaaba
Suppose gene 2 was chosen to be exchanged. In this case the following offspring is formed:
012345678012345678012345678
/aa-abaaa Q+aQbabaa/Q*+aaaab
/-*/abbab/a*bbaaab -Q/Qbaaba
The newly created individuals contain genes from both parents. Note that with this kind of recombination, similar genes can be exchanged but, most of the time, the exchanged genes are very different and new material is introduced into the population.
It is worth noting that this operator is unable to create new genes: the individuals created are different arrangements of existing genes. In fact, when gene recombination is used as the unique source of genetic variation, more complex problems can only be solved using very large initial populations in order to provide for the necessary diversity of genes (see section 6.1). However, the creative power of GEP is based not only in the shuffling of genes or building blocks, but also in the constant creation of new genetic material.

6. Six examples of gene expression programming in problem solving
The suite of problems chosen to illustrate the functioning of this new algorithm is quite varied, including not only problems from different fields (symbolic regression, planning, Boolean concept learning, and cellular automata rules) but also problems of great complexity (cellular automata rules for the density-classification task).

6.1. Symbolic regression
The objective of this problem is the discovery of a symbolic expression that satisfies a set of fitness cases. Consider we are given a sampling of the numerical values from the function
y = a^4 + a^3 + a^2 + a (6.1)
over 10 chosen points and we want to find a function fitting those values within 0.01 of the correct value.
First, the set of functions F and the set of terminals T must be chosen. In this case F = {+, -, *, /} and T = {a}. Then
120102030405060708090100
0 20 40 60 80 100 120 140 160 180 200 Population size Success rate (%)
0102030405060708090
0 1 02 03 04 05 06 07 08 09 0 1 0 0
Chromosome length Success rate (%) the structural organization of chromosomes, namely the
###基因重组 ###两点重组 ###多基因染色体 ###基因表达编程 (GEP) ###符号回归 ###细胞自动机 ###遗传变异 ###种群多样性 ###染色体结构 ###适应度函数
&&&&
over 10 chosen points and we want to find a function fitting those values within 0.01 of the correct value. First, the set of functions F and the set of terminals T must be chosen. In this case F = {+, -, *, /} and T = {a}. Then the structural organization of chromosomes, namely the length of the head and the number of genes, is chosen. It is advisable to start with short, single-gene chromosomes and then gradually increase h. Figure 6 shows such an analysis for this problem. A population size P of 30 individuals and an evolutionary time G of 50 generations were used. A pm equivalent to two one-point mutations per chromosome and a p1r = 0.7 were used in all the experiments in order to simplify the analysis. The set of fitness cases is shown in Table 1 and the fitness was evaluated by equation (4.1a), being M = 100. If |C(i,j)-Tj| is equal to or less than 0.01 (the precision), then |C(i,j)-Tj| = 0 and f(i,j)= 100; thus for Ct = 10, fmax = 1000.

Note that GEP can be useful in searching the most parsimonious solution to a problem. For instance, the chromosome *++/**aaaaaaa with h = 6 codes for the ET: which is equivalent to the target function. Note also that GEP can efficiently evolve solutions using large values of h, that is, it is capable of evolving large and complex sub-ETs. It is worth noting that the most compact genomes are not the most efficient. Therefore a certain redundancy is fundamental to efficiently evolve good programs.

In another analysis, the relationship between success rate and population size P, using an h = 24 was studied (Figure 7). These results show the supremacy of a genotype/phenotype representation, as this single-gene system, which is equivalent to GP, greatly surpasses that technique [9]. However, GEP is much more complex than a single-gene system because GEP chromosomes can encode more than one gene (see Figure 8).

Suppose we could not find a solution after the analysis shown in Figure 6. Then we could increase the number of genes, and choose a function to link them. For instance, we could choose an h = 6 and then increase the number of genes.

Table 1 Set of fitness cases for the symbolic regression problem.
Figure 6. Variation of success rate (Ps) with chromosome length. For this analysis G = 50, P = 30, and Ps was evaluated over 100 identical runs.
Figure 7. Variation of success rate (Ps) with population size. For this analysis G = 50, and a medium value of 49 for chromosome length (h = 24) was used. Ps was evaluated over 100 identical runs.
###GEP ###基因表达式编程 ###染色体 ###基因 ###进化算法 ###种群规模 ###成功率 ###适应度 ###符号回归 ###基因型/表型表示
&&&&
GEP（Gene Expression Programming）是一种基因表达编程技术，其单基因系统（等同于GP）在性能上远超传统技术。然而，GEP比单基因系统复杂得多，因为GEP染色体可以编码多个基因（参见图8）。

如果在图6所示的分析后仍未找到解决方案，可以增加基因数量并选择一个函数来连接它们。例如，可以选择h=6，然后逐渐增加基因数量。图8显示了此问题的成功率如何取决于基因数量。在此分析中，pm被修改以编码连接函数。在这种情况下，对于每个问题，理想的连接函数将在适应过程中找到。

例如，考虑一个由3个基因通过加法连接组成的多基因系统。如图8所示，在这种情况下，成功率的最大值为100%。图10显示了表2第1列中总结的实验的运行0中种群的平均适应度和最佳个体的适应度进展。在此运行中，在第11代找到了一个正确的解决方案。子ET通过加法连接：
012345678901201234567890120123456789012
**-*a+aaaaaaa++**a*aaaaaaa*+-a/aaaaaaaa
在数学上对应于目标函数（每个子ET的贡献在括号中表示）：
y = (a4) + (a3 + a2 + a) + (0) = a4 + a3 + a2 + a.

对该程序的详细分析表明，对于手头的问题，某些操作是冗余的，例如加0或乘1。然而，这些不必要的簇甚至伪基因（如基因3）的存在对于更适应个体的进化很重要（比较图6和图8中，紧凑的单基因系统（h=6）与其他基因更多且h大于6的非紧凑系统的成功率）。

图10（以及下面的图12、13和17）中的平均适应度图表明了不同的进化策略。图8：成功率（Ps）随基因数量的变化。在此分析中，G=50，P=30，h=6（基因长度为13）。Ps在100次相同运行中进行评估。
每个染色体相当于两次单点突变，p1r=0.2，p2r=0.5，pgr=0.1，pis=0.1，pris=0.1，pgt=0.1，并使用了长度为1、2和3的三个转座子（IS和RIS元件）。请注意，GEP可以很好地应对基因过多的情况：10基因系统的成功率仍然非常高（47%）。

图9显示了另一个重要关系：成功率如何取决于进化时间。与GP（通常在51代后不再有太多发现）不同，在GEP中，种群可以无限期地适应和进化，因为新的材料不断被引入基因库。

最后，假设多基因系统与子ET。
###基因表达编程 ###GEP ###基因系统 ###染色体 ###适应度 ###进化时间 ###遗传算法 ###多基因系统 ###单基因系统 ###成功率 ###转座子 ###基因库
&&&&
very well with an excess of genes: the success rate for the 10-genic system is still very high (47%).

In Figure 9 another important relationship is shown: how the success rate depends on evolutionary time. In contrast to GP where 51 generations are the norm, for after that nothing much can possibly be discovered [7], in GEP, populations can adapt and evolve indefinitely because new material is constantly being introduced into the genetic pool.

Finally, suppose that the multigenic system with sub-ETs linked by addition could not evolve a satisfactory solution. Then we could choose another linking function, for instance, multiplication. This process is repeated until a good solution has been found.

As stated previously, GEP chromosomes can be easily Figure 9. Variation of success rate (Ps) with the number of generations. For this analysis P = 30, pm = 0.051, p1r = 0.7 and a chromosome length of 79 (a single-gene chromosome with h = 39) was used. Ps was evaluated over 100 identical runs.

Table 2 Parameters for the symbolic regression (SR), sequence induction (SI), sequence induction using ephemeral random constants (SI*), block stacking (BS), and 11-multiplexer (11-M) problems. Figure 10. Progression of average fitness of the population and the fitness of the best individual for run 0 of the experiment summarized in Table 2, column 1 (symbolic regression). dynamics for GEP populations. The oscillations on average fitness, even after the discovery of a perfect solution, are unique to GEP. A certain degree of oscillation is due to the small population sizes used to solve the problems presented in this work. However, an identical pattern is obtained using larger population sizes. Figure 11 compares six evolutionary dynamics in populations of 500 individuals for 500 generations. Plot 1 (all operators active) shows the progression of average fitness of an experiment identical to the one summarized in Table 2, column 1, that is, with all the genetic operators switched on. The remaining dynamics were obtained for mutation alone (Plot 2), for gene recombination combined with gene transposition (Plot 3), for one-point recombination (Plot 4), two-point recombination (Plot 5), and gene recombination (Plot 6).

It is worth noticing the homogenizing effect of all kinds of recombination. Interestingly, this kind of pattern is similar to the evolutionary dynamics of GAs and GP populations [9, 10]. Also worth noticing is the plot for gene recombination alone (Figure 11, Plot 6): in this case a perfect solution was not found. This shows that sometimes it is impossible to find a perfect solution only by shuffling existing building blocks, as is done in all GP implementations without mutation. Indeed, GEP gene recombination is similar in effect to GP recombination, for it permits exclusively the recombination of
###GEP ###GP ###基因表达编程 ###遗传编程 ###进化算法 ###基因重组 ###基因转座 ###符号回归 ###序列归纳 ###多路复用器
&&&&
of pattern is similar to the evolutionary dynamics of GAs and GP populations [9,10]. Also worth noticing is the plot for gene recombination alone (Figure 11, Plot 6): in this case a perfect solution was not found. This shows that sometimes it is impossible to find a perfect solution only by shuffling existing building blocks, as is done in all GP implementations without mutation. Indeed, GEP gene recombination is similar in effect to GP recombination, for it permits exclusively the recombination of mathematically concise blocks. Note that even a more generalized shuffling of building blocks (using gene recombination combined with gene transposition) results in oscillatory dynamics (Figure 11, Plot 3).

Generations Fitness (max 1000) Best Ind Avg fitness
SR SI SI* BS 11-M
Number of runs 100 100 100 100 100
Number of generations 50 100 100 100 400
Population size 30 50 50 30 250
Number of fitness cases 10 10 10 10 160
Head length 6 6 7 4 1
Number of genes 3 7 8 3 27
Chromosome length 39 91 184 27 27
Mutation rate 0.051 0.022 0.011 0.074 0.074
One-point recombination rate 0.2 0.7 0.5 0.1 0.7
Two-point recombination rate 0.5 0.1 0.2 -- --
Gene recombination rate 0.1 0.1 0.1 0.7 --
IS transposition rate 0.1 0.1 0.1 0.1 --
IS elements length 1,2,3 1,2,3 1 1 --
RIS transposition rate 0.1 0.1 0.1 0.1 --
RIS elements length 1,2,3 1,2,3 1 1 --
Gene transposition rate 0.1 0.1 0.1 -- --
Random constants mutation rate -- 0.01 -- -- 0.01
Selection range 100 -- 20% 20% --
Dc specific IS transposition rate -- -- -- -- --
Error 0.0% 0.0% -- -- --
Success rate 1 0.83 0.31 0.7 0.57

6.2. Sequence induction and the creation of constants
The problem of sequence induction is a special case of symbolic regression where the domain of the independent variable consists of the nonnegative integers. However, the sequence chosen is more complicated than the expression used in symbolic regression, as different coefficients were used.
The solution to this kind of problem involves the discovery of certain constants. Here two different approaches to the problem of constant creation are shown: one without using ephemeral random constants [9], and another using ephemeral random constants.
In the sequence 1, 15, 129, 547, 1593, 3711, 7465, 13539, 22737, 35983, 54321,..., the nth (N) term is
N = a + a*n + a*n^2 + a*n^3 + a*n^4 + a*n^5
where a_n consists of the nonnegative integers 0, 1, 2, 3,....
For this problem F = {+, -, *, /} and T = {a}. The set of fitness cases is shown in Table 3 and the fitness was evaluated by equation (4.1b), being M = 20%. Thus, if the 10 fitness cases were computed exactly, f_max = 200.
Figure 12 shows the progression of average fitness of the population and the fitness of the best individual for run 1 of the experiment summarized in Table 2, column 2. In this run, a perfect solution was found in generation 81 (the sub-ETs are linked by addition).
###遗传算法 (GAs) ###遗传编程 (GP) ###基因表达编程 (GEP) ###基因重组 ###基因转座 ###突变率 ###序列归纳 ###符号回归 ###常量创建 ###适应度函数 ###种群规模 ###迭代次数
&&&&
在表3中，适应度通过公式(4.1b)评估，其中M = 20%。因此，如果精确计算10个适应度案例，fmax = 200。

图12显示了表2第2列中实验run1的种群平均适应度以及最佳个体适应度的进展。在此运行中，在第81代找到了一个完美的解决方案（子ET通过加法链接）：
y = (a^2+a)+(a^4-a^3)+(4a^4+4a^3)+(a^2+2a-1)+(a^3)+(-a)+(a^2+2)。
这在数学上对应于目标序列（每个子ET的贡献在括号中表示）。

如表2第2列所示，使用第一种方法解决此问题的成功概率为0.83。请注意，所有常数都是由算法从头创建的。在实际问题中，这种方法似乎更具优势，因为首先，我们事先不知道需要什么样的常数；其次，终端集中的元素数量要少得多，从而降低了问题的复杂性。

然而，瞬时随机常数可以很容易地在GEP中实现。为此，创建了一个额外的域Dc。在结构上，Dc位于尾部之后，长度等于t，由用于表示瞬时随机常数的符号组成。对于每个基因，常数在开始时创建。

表3：序列归纳问题的适应度案例集。
图11：GEP种群可能的进化动态。在此分析中，P = 500。图表显示了种群平均适应度的进展。图1：所有操作符都已开启，速率如表2第1列所示；在这种情况下，在第1代找到了一个完美的解决方案。图2：仅突变，pm = 0.051；在这种情况下，在第3代找到了一个完美的解决方案。图3：仅基因重组，pgr = 0.7，加上基因转座，pgt = 0.2；在这种情况下，在第2代找到了一个完美的解决方案。图4：仅单点重组，p1r = 0.7；在这种情况下，在第3代找到了一个完美的解决方案。图5：仅两点重组，p2r = 0.7；在这种情况下，在第1代找到了一个完美的解决方案。图6：仅基因重组，pgr = 0.7；在这种情况下，未找到完美的解决方案：最佳运行的适应度为980，在第2代找到。
###基因表达编程（GEP） ###适应度评估 ###进化算法 ###种群平均适应度 ###基因重组 ###基因转座 ###突变 ###随机常数 ###序列归纳问题 ###完美解决方案
&&&&
首先，我们事先不知道需要什么样的常数，其次，终端集中的元素数量要小得多，从而降低了问题的复杂性。
然而，瞬时随机常数可以很容易地在GEP中实现。为此，创建了一个额外的域Dc。在结构上，Dc位于尾部之后，长度等于t，由用于表示瞬时随机常数符号组成。
对于每个基因，常数在运行开始时创建，但其循环由遗传算子保证。此外，还创建了一个特殊的突变算子，允许在随机常数集中永久引入变异。还创建了一个特定领域的IS转座，以确保常数的有效洗牌。请注意，基本遗传算子不受Dc影响：只需保持每个区域的边界，不要混合不同的字母表。
图12. 实验运行1中群体平均适应度和最佳个体适应度的进展，总结在表2，第2列（无瞬时随机常数的序列归纳）。
考虑一个h=7的单基因染色体：
*?**?+?aa??a?a?63852085 (6.3)
其中“？”表示瞬时随机常数。这种染色体的表达方式与之前完全相同，得到：
ET中的“？”符号随后从左到右、从上到下被Dc中的符号替换，得到：
与这些符号对应的值保存在一个数组中。为简单起见，符号表示的数字表示在数组中的顺序。例如，对于10个元素的数组：
A = {-0.004, 0.839, -0.503, 0.05, -0.49, -0.556, 0.43, -0.899, 0.576, -0.256}
上述染色体(6.3)给出：
为了使用瞬时随机常数F = {+, -, *}，T = {a, ?}，随机常数集R = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}，以及瞬时随机常数“？”范围为整数0, 1, 2, 和3来解决当前问题。
每次运行使用的参数如表2，第3列所示。在此实验中，第一个解决方案在运行8的第91代中找到（子ET通过加法链接）：
Gene 0: -??*a-*aaa?a?aa26696253
A0 = {3, 1, 0, 0, 3, 3, 2, 2, 2, 3}
Gene 1: *-aa-a-???a?aaa73834168
A1 = {0, 1, 2, 3, 1, 3, 0, 0, 1, 3}
Gene 2: +a??-+??aaaa?aa43960807
A2 = {1, 2, 1, 3, 3, 2, 2, 2, 1, 3}
Gene 3: *a***+aa?a??aaa20546809
A3 = {3, 0, 1, 3, 0, 2, 2, 2, 2, 0}
Gene 4: *a***+aa?aa?aaa34722724
A4 = {2, 3, 3, 2, 1, 3, 0, 0, 2, 3}
Gene 5: *a*++*+?aa??a?a54218512
A5 = {1, 3, 3, 1, 0, 0, 2, 0, 0, 2}
Gene 6: +a*?a*-a?aaa??a94759218
A6 = {3, 0, 0, 2, 1, 1, 3, 1, 3, 2}
Gene 7: +-?a*a??a?aa??a69085824
A7 = {2, 2, 3, 1, 3, 1, 0, 0, 1, 0}
###瞬时随机常数 ###GEP ###遗传算子 ###突变算子 ###IS转座 ###适应度 ###单基因染色体 ###随机常数集 ###序列归纳 ###基因
&&&&
Gene 2: A2 = {1, 2, 1, 3, 3, 2, 2, 2, 1, 3}
Gene 3: A3 = {3, 0, 1, 3, 0, 2, 2, 2, 2, 0}
Gene 4: A4 = {2, 3, 3, 2, 1, 3, 0, 0, 2, 3}
Gene 5: A5 = {1, 3, 3, 1, 0, 0, 2, 0, 0, 2}
Gene 6: A6 = {3, 0, 0, 2, 1, 1, 3, 1, 3, 2}
Gene 7: A7 = {2, 2, 3, 1, 3, 1, 0, 0, 1, 0}
and mathematically corresponds to the target function (the contribution of each sub-ET is indicated in brackets):
y = (-2)+(-3a)+(a+3)+(a4+3a3)+(4a4)+(a3+3a2)+(3a).
As shown in column 3 of Table 2, the probability of success for this problem is 0.31, considerably lower than the 0.83 of the first approach. Furthermore, only the prior knowledge of the solution enabled us, in this case, to correctly choose the random constants. Therefore, for real-world applications where the magnitude and type of coefficients is unknown, it is more appropriate to let the system find the constants for itself. However, for some numerical applications the discovery of constants is fundamental and they can be easily created as indicated here.

6.3. Block stacking
In block stacking, the goal is to find a plan that takes any initial configuration of blocks randomly distributed between the stack and the table and places them in the stack in the correct order. In this case, the blocks are the letters of the word “universal”. (Although the word universal was used as illustration, in this version the blocks being stacked may have identical labels like, for instance, in the word “individual”.)
The functions and terminals used for this problem consisted of a set of actions and sensors, being F = {C, R, N, A} (move to stack, remove from stack, not, and do until true, respectively), where the first three take one argument and “A” takes two arguments. In this version, the “A” loops are processed at the beginning and are solved in a particular order (from bottom to top and from left to right). The action argument is executed at least once despite the state of the predicate argument and each loop is executed only once, timing out after 20 iterations. The set of terminals consisted of three sensors {u, t, p} (current stack, top correct block, and next needed block, respectively). In this version, “t” refers only to the block on the top of the stack and whether it is correct or not; if the stack is empty or has some blocks, all of them correctly stacked, the sensor returns True, otherwise it returns False; and “p” refers obviously to the next needed block immediately after “t”.
A multigenic system composed of three genes of length
###Block stacking ###Target function ###Random constants ###Numerical applications ###Multigenic system ###Actions ###Sensors ###Terminals ###Probability of success ###Real-world applications
&&&&
r 20 iterations. The set of terminals consisted of three sensors {u, t, p} (current stack, top correct block, and next needed block, respectively). In this version, “t” refers only to the block on the top of the stack and whether it is correct or not; if the stack is empty or has some blocks, all of them correctly stacked, the sensor returns True, otherwise it returns False; and “p” refers obviously to the next needed block immediately after “t”.

A multigenic system composed of three genes of length 9 was used in this problem. The linking of the sub-ETs consisted of the sequential execution of each sub-ET or sub-plan. For instance, if the first sub-ET empties all the stacks, the next sub-ET may proceed to fill them, and so on. The fitness was determined against 10 fitness cases (initial configurations of blocks). For each generation, an empty stack plus nine initial configurations with one to nine letters in the stack were randomly generated. The empty stack was used to prevent the untimely termination of runs, as a fitness point was attributed to each empty stack (see below). However, GEP is capable of efficiently solving this problem using 10 random initial configurations (results not shown).

The fitness function was as follows: for each empty stack one fitness point was attributed; for each partially and correctly packed stack (i.e., with 1 to 8 letters in the case of the word “universal”) two fitness points were attributed; and for each completely and correctly stacked word 3 fitness points were attributed. Thus, the maximum fitness was 30. The idea was to make the population of programs hierarchically evolve solutions toward a perfect plan. And, in fact, usually the first useful plan discovered empties all the stacks, then some programs learn how to partially fill those empty stacks, and finally a perfect plan is discovered that fills the stacks completely and correctly (see Figure 13).

Figure 13 shows the progression of average fitness of the population and the fitness of the best individual for run 2 of the experiment summarized in Table 2, column 4. In this run, a perfect plan was found in generation 50:
012345678012345678012345678
ARCuptppuApNCptuutNtpRppptp

Note that the first sub-plan removes all the blocks and stacks a correct letter; the second sub-plan correctly stacks all the remaining letters; and the last sub-plan does nothing. It should be emphasized that the plans with maximum fitness evolved are in fact perfect, universal plans: each generation they are tested against nine randomly generated initial configurations, more than sufficient to allow the algorithm to
18Figure 13. Progression of average fitness of the population and the fitness of the best individual for run 2 of the experiment summarized in Table 2, column 4 (block stacking).
###基因表达编程 (GEP) ###适应度函数 ###多基因系统 ###传感器 ###堆栈操作 ###块堆叠 ###进化算法 ###初始配置 ###子计划 ###普遍计划
&&&&
an correctly stacks all the remaining letters; and the last sub-plan does nothing. It should be emphasized that the plans with maximum fitness evolved are in fact perfect, universal plans: each generation they are tested against nine randomly generated initial configurations, more than sufficient to allow the algorithm to generalize the problem (as shown in Figure 13, once reached, the maximum fitness is maintained). Indeed, with the fitness function and the kind of fitness cases used, all plans with maximum fitness are universal plans.

As shown in the fourth column of Table 2, the probability of success for this problem is very high (0.70) despite using nine (out of 10) random initial configurations. It is worth noting that GP uses 167 fitness cases, cleverly constructed to cover the various classes of possible initial configurations [9]. Indeed, in real-life applications it is not always possible to predict the kind of cases that would make the system discover a solution. So, algorithms capable of generalizing well in face of random fitness cases are more advantageous.

**6.4. Evolving cellular automata rules for the density-classification problem**

Cellular automata (CA) have been studied widely as they are idealized versions of massively parallel, decentralized computing systems capable of emergent behaviors. These complex behaviors result from the simultaneous execution of simple rules at multiple local sites. In the density-classification task, a simple rule involving a small neighborhood and operating simultaneously in all the cells of a one-dimensional cellular automaton, should be capable of making the CA converge into a state of all 1s if the initial configuration (IC) has a higher density of 1s, or into a state of all 0s if the IC has a higher density of 0s.

The ability of GAs to evolve CA rules for the density-classification problem was intensively investigated [12-15], but the rules discovered by the GA performed poorly and were far from approaching the accuracy of the GKL rule, a human-written rule. GP was also used to evolve rules for the density-classification task [16], and a rule was discovered that surpassed the GKL rule and other human-written rules.

This section shows how GEP is successfully applied to this difficult problem. The rules evolved by GEP have accuracy levels of 82.513% and 82.55%, thus exceeding all human-written rules and the rule evolved by GP.

**6.4.1. The density-classification task**

The simplest CA is a wrap-around array of N binary-state cells, where each cell is connected to r neighbors from both sides. The state of each cell is updated by a defined rule. The rule is applied simultaneously in all the cells, and the process is iterated for t time steps.

In the most frequently studied version of this problem,
###通用计划 ###遗传编程 (GP) ###基因表达式编程 (GEP) ###细胞自动机 (CA) ###密度分类问题 ###规则演化 ###机器学习 ###算法泛化 ###并行计算 ###分布式系统

---
**说明：**

*   **清洗：**
    *   删除了页眉页脚（"18 Figure 13."）。
    *   删除了HTML标签（原文中没有明显的HTML标签，但如果存在会删除）。
    *   修正了段落分割，将连续的文本根据语义和标点符号进行了合理分段。
    *   没有发现明显的乱码。
    *   保留了所有重要信息、数据（如0.70的成功概率，82.513%和82.55%的准确率）和技术术语。
    *   加粗了小节标题，使其更清晰。

*   **关键词提取：**
    *   **经营模式/产业类型：** 文中未直接提及具体的经营模式或产业类型，更多是关于算法和技术研究。
    *   **技术应用：** 遗传编程 (GP)、基因表达式编程 (GEP)、细胞自动机 (CA) 是核心技术。密度分类问题是这些技术的具体应用场景。规则演化是这些技术实现目标的方式。
    *   **政策措施：** 未提及。
    *   **专业术语：** 通用计划 (universal plans)、健身函数 (fitness function)、初始配置 (initial configurations)、密度分类问题 (density-classification problem)、细胞自动机 (cellular automata)、遗传算法 (GAs)、基因表达式编程 (GEP)、GKL规则 (GKL rule)、并行计算 (massively parallel computing)、分布式系统 (decentralized computing systems)、算法泛化 (generalize the problem)。
    *   **地理标识：** 无。

    综合以上，提取了与技术应用、算法、模型和相关概念紧密联系的关键词。
&&&&
GEP演化出的准确率达到82.513%和82.55%，超过了所有人工编写的规则和GP演化出的规则。

6.4.1. 密度分类任务
最简单的元胞自动机（CA）是一个由N个二元状态单元组成的环绕数组，每个单元与两侧的r个邻居连接。每个单元的状态由定义的规则更新。该规则同时应用于所有单元，并重复该过程t个时间步。

在该问题最常研究的版本中，N=149，邻域为7（中心单元由“u”表示；左侧的r=3个单元由“c”、“b”和“a”表示；右侧的r=3个单元由“1”、“2”和“3”表示）。因此，该问题规则空间的搜索规模是巨大的2^128。图14显示了一个N=11的CA，以及应用特定转换规则后元胞自动机“u”的更新状态。

图14. 一个一维、二元状态、r=3的元胞自动机，N=11。箭头表示周期性边界条件。更新状态仅显示中心单元。还显示了用于表示邻域的符号。

密度分类任务包括通过使系统分别收敛到全1状态（时空图中的黑色或“开”单元）和全0状态（白色或“关”单元），来正确判断初始配置（IC）是包含多数1还是多数0。由于IC的密度是N个参数的函数，因此具有有限信息和通信的局部单元的动作必须相互协调才能正确分类IC。事实上，找到表现良好的规则是一个挑战，并且使用了几种算法来演化出更好的规则[14-17]。通过在GA演化规则和IC之间采用协同演化方法，发现了性能分别为86.0%（协同演化2）和85.1%（协同演化1）的最佳规则[17]。然而，本节的目的是比较GEP在应用于困难问题时与GA和GP的性能。

最后，当一个独立的程序能够正确分类多数为1和多数为0的IC时，将一个等于IC数量C的奖励添加到正确分类的IC数量中，此时f = i + C。例如，如果一个程序正确分类了两个IC，一个多数为1，另一个多数为0，它将获得2+25=27个适应度点。

本次实验共进行了7次运行。在运行5的第27代，一个独立个体演化出的适应度为44：
0123456789012345678901234567890123456789012345678901
OAIIAucONObAbIANIb1u23u3a12aacb3bc21aa2baabc3bccuc13
请注意，ORF在位置28结束。该程序具有一个。
###元胞自动机 ###密度分类 ###基因表达式编程 (GEP) ###遗传算法 (GA) ###协同演化 ###规则演化 ###初始配置 (IC) ###二元状态 ###周期性边界条件 ###适应度函数 ###机器学习 ###优化算法
&&&&
在本次实验中，总共进行了7次运行。在第5次运行的第27代，一个个体进化出了44的适应度：
0123456789012345678901234567890123456789012345678901
OAIIAucONObAbIANIb1u23u3a12aacb3bc21aa2baabc3bccuc13
请注意，ORF在位置28结束。该程序在149x298的格子上对100,000个无偏初始配置（ICs）进行测试，准确率为0.82513，优于GP规则在149x320格子上测试的0.824准确率[16, 17]。该规则（GEP 1）的规则表如表5所示。图15显示了该新规则的三个时空图。

作为比较，GP使用了51,200个个体和1000个ICs，进行了51代，总共进行了51,200 * 1,000 * 51 = 2,611,200,000次适应度评估，而GEP仅进行了30 * 25 * 50 = 37,500次适应度评估。因此，在这个问题中，GEP的性能比GP高出四个数量级以上（69,632倍）。

在另一个实验中，获得了比GEP 1略好的规则，准确率为0.8255。同样，其性能是在149x298的格子上对100,000个无偏ICs进行测试后确定的。在这种情况下，F = {I, M}（“I”代表IF，“M”代表具有三个参数的多数函数），T显然是相同的。在这种情况下，使用了总共100个无偏ICs和通过IF连接的三个基因染色体（sub-ETs）。每次运行使用的参数如表4的第二列所示。

适应度函数通过引入排名系统进行了轻微修改，其中能够正确分类2到3/4的ICs的个体获得一个等于C的奖励；如果正确分类了3/4到17/20的ICs，则获得两个C的奖励；如果正确分类了超过17/20的ICs，则获得三个C的奖励。此外，在此实验中，能够仅正确分类一种情况的个体（尽管不是不加区分地）被区分开来，其适应度等于i。事实上，GEP确实进化出了比GP规则更好的规则，使用的计算资源比GP少四个数量级以上。

6.4.2. 两个基因表达编程发现的规则
在一个实验中，F = {A, O, N, I}（“A”代表布尔函数AND，“O”代表OR，“N”代表NOT，“I”代表IF），T = {c, b, a, u, 1, 2, 3}。每次运行使用的参数如表4的第1列所示。

表4 密度分类任务的参数。
适应度是根据25个无偏ICs（即每个单元格有相同概率为1或0的ICs）进行评估的。在这种情况下，适应度是系统在2xN时间步后正确稳定到全0或全1配置的ICs数量i的函数，并且它是...
###基因表达编程 ###遗传编程 ###适应度评估 ###密度分类 ###机器学习 ###算法优化 ###计算资源 ###准确率 ###布尔函数 ###初始配置
&&&&
The parameters used per run are shown in Table 4, column 1.
Table 4 Parameters for the density-classification task.
The fitness was evaluated against a set of 25 unbiased ICs (i.e., ICs with equal probability of having a 1 or a 0 at each cell). In this case, the fitness is a function of the number of ICs i for which the system stabilizes correctly to a configuration of all 0s or 1s after 2x N time steps, and it was designed in order to privilege individuals capable of correctly classifying ICs both with a majority of 1s and 0s. Thus, if the system converged, in all cases, indiscriminately to a configuration of 1s or 0s, only one fitness point was attributed. If, in some cases, the system correctly converged either to a configuration of 0s or 1s, f = 2. In addition, rules converging to an alternated pattern of all 1s and all 0s were eliminated, as they are easily discovered and invade the populations impeding the discovery of good rules.
Table 5 Description of the two new rules (GEP1 and GEP2) discovered using GEP for the density-classification problem. The GP rule is also shown. The output bits are given in lexicographic order starting with 0000000 and finishing with 1111111.
00010001 00000000 01010101 00000000 00010001 00001111 01010101 00001111
00010001 11111111 01010101 11111111 00010001 11111111 01010101 11111111
00000000 01010101 00000000 01110111 00000000 01010101 00000000 01110111
00001111 01010101 00001111 01110111 11111111 01010101 11111111 01110111
00000101 00000000 01010101 00000101 00000101 00000000 01010101 00000101
01010101 11111111 01010101 11111111 01010101 11111111 01010101 11111111
GEP1
GEP2
GP rule
Number of generations 50 50
Population size 30 50
Number of ICs 25 100
Head length 17 4
Number of genes 1 3
Chromosome length 52 39
Mutation rate 0.038 0.05
1-Point recombination rate 0.5 0.7
IS transposition rate 0.2 --
IS elements length 1,2,3 --
RIS transposition rate 0.1 --
RIS elements length 1,2,3 --
By generation 43 of run 10, an individual evolved with fitness 393:
Its rule table is shown in Table 5. Figure 16 shows three space-time diagrams for this new rule (GEP2). Again, in this case the comparison with GP shows that GEP outperforms GP by a factor of 10,444.
6.5. Boolean concept learning
The GP rule and the 11-multiplexer are, respectively, boolean functions of seven and 11 activities. Whereas the solution for the 11-multiplexer is a well-known boolean function, the solution of the GP rule is practically unknown, as the program evolved by GP [16] is so complicated that it is impossible to know what the program really does.
This section shows how GEP can be efficiently applied
###密度分类任务 ###基因表达编程 (GEP) ###遗传编程 (GP) ###布尔概念学习 ###适应度评估 ###初始配置 (ICs) ###规则发现 ###种群规模 ###变异率 ###重组率

---
**说明：**

*   **清洗要求：**
    *   删除了页眉页脚（如 "ents OR ###“N” represents NOT ###and“I” stands for IF) and T = {c ###b ###a ###u ###1 ###2 ###3}." 这部分内容，它看起来是前一页的遗留或无关信息）。
    *   删除了HTML标签和多余空白。
    *   修正了段落分割，使文本更具可读性。
    *   清理了乱码（原文本中没有明显的乱码，但保留了处理乱码的原则）。
    *   保留了所有重要信息、数据和专业术语。

*   **关键词提取要求：**
    *   **经营模式/产业类型：** 文本主要涉及科学研究和算法优化，不直接涉及经营模式或产业类型。
    *   **技术应用：** 基因表达编程 (GEP) ###遗传编程 (GP) ###布尔概念学习 ###密度分类任务 ###规则发现。
    *   **政策措施：** 文本不涉及政策措施。
    *   **专业术语和地理标识：** 基因表达编程 (GEP) ###遗传编程 (GP) ###密度分类任务 ###布尔概念学习 ###适应度评估 ###初始配置 (ICs) ###规则发现 ###种群规模 ###变异率 ###重组率。没有地理标识。

**关键词选择理由：**

*   **密度分类任务 (density-classification task)：** 文本的核心研究问题。
*   **基因表达编程 (GEP)：** 文本中重点介绍和应用的技术。
*   **遗传编程 (GP)：** 作为与GEP进行比较的基准技术。
*   **布尔概念学习 (Boolean concept learning)：** GEP的应用领域之一。
*   **适应度评估 (fitness evaluation)：** 算法优化中的关键环节。
*   **初始配置 (ICs)：** 实验中用于评估系统性能的输入数据。
*   **规则发现 (rule discovery)：** GEP和GP的目标之一。
*   **种群规模 (Population size)：** 算法参数，影响模型性能。
*   **变异率 (Mutation rate)：** 算法参数，影响模型性能。
*   **重组率 (recombination rate)：** 算法参数，影响模型性能。

这些关键词涵盖了文本的主要内容、研究方法和技术细节。
&&&&
The comparison with GP shows that GEP outperforms GP by a factor of 10,444.6.5. Boolean concept learning.
The GP rule and the 11-multiplexer are, respectively, boolean functions of seven and 11 activities. Whereas the solution for the 11-multiplexer is a well-known boolean function, the solution of the GP rule is practically unknown, as the program evolved by GP [16] is so complicated that it is impossible to know what the program really does.
This section shows how GEP can be efficiently applied to evolve boolean expressions of several arguments. Furthermore, the structural organization of the chromosomes used to evolve solutions for the 11-multiplexer is an example.

Figure 15. Three space-time diagrams describing the evolution of CA states for the GEP1 rule. The number of 1s in the IC (0) is shown above each diagram. In (a) and (b) the CA correctly converged to a uniform pattern; in (c) it converged wrongly to a uniform pattern.
Figure 16. Three space-time diagrams describing the evolution of CA states for the GEP2 rule. The number of 1s in the IC (0) is shown above each diagram. In (a) and (b) the CA converges, respectively, to the correct configuration of all 0s and all 1s; in (c) the CA could not converge to a uniform pattern.

21 of a very simple organization that can be used to efficiently solve certain problems. For example, this organization (one-element genes linked by IF) was successfully used to evolve CA rules for the density-classification problem, discovering better rules than the GKL rule (results not shown).

6.5.1. The genetic programming rule problem.
For this problem F = {N, A, O, X, D, R, I, M} (representing, respectively: NOT, AND, OR, XOR, NAND, NOR, IF, and Majority, the first being a function of one argument, the second through fifth are functions of two arguments, and the last two are functions of three arguments), and T = {c, b, a, u, 1, 2, 3}. The rule table (2^7=128 fitness cases) is shown in Table 5 and the fitness was evaluated by equation (4.2). Thus, f_max = 128.
Three different solutions were discovered in one experiment:
MA3OOAMOAuOMRa1cc3cubcc2cu11ba2aacb331ua122uu1X3RRMIMODIAIAAI3cauuc313bub2uc33ca12u233c22bcb
MMOIOcXOMa3AXAu3cc112ucbb3331uac3cu3auubuu2ab1
Careful analysis of these programs shows that the GP rule is, like the GKL rule, a function of five arguments: c, a, u, 1, and 3.

6.5.2. The 11-multiplexer problem.
The task of the 11-bit boolean multiplexer is to decode a 3-bit binary address (000, 001, 010, 011, 100, 101, 110, 111) and return the value of the corresponding data register (d0, d1, d2, d3, d4, d5, d6, d7). Thus, the boolean 11-multiplexer is a function of 11 arguments: three, a0 to a2, determine the address, and eight, d0 to d7, determine the answer. As GEP uses single-character chromosomes, T = {a, b, c, 1, 2, 3, 4, 5, 6, 7, 8} which correspond, respectively, to {a0, a1, a2, d0, d1, d2, d3, d4, d5, d6, d7}.
There are 2^11 = 2048 possible combinations for the 11.
###GEP ###GP ###布尔概念学习 ###11-multiplexer ###遗传编程规则问题 ###密度分类问题 ###染色体 ###空间-时间图 ###CA状态 ###适应度函数
&&&&
(000, 001, 010, 011, 100, 101, 110, 111) 并返回相应数据寄存器 (d0, d1, d2, d3, d4, d5, d6, d7) 的值。因此，布尔11-多路复用器是11个参数的函数：其中三个，a0到a2，确定地址；八个，d0到d7，确定答案。由于GEP使用单字符染色体，T = {a, b, c, 1, 2, 3, 4, 5, 6, 7, 8} 分别对应 {a0, a1, a2, d0, d1, d2, d3, d4, d5, d6, d7}。

布尔11-多路复用器函数有 2^11 = 2048 种可能的参数组合。对于这个问题，每一代都使用2048种组合的随机抽样作为适应度案例来评估适应度。适应度案例按地址分组，对于每个地址，每一代都使用20个随机组合的子集。因此，每一代总共使用160个随机适应度案例作为适应环境。在这种情况下，程序的适应度是返回正确布尔值的适应度案例的数量，加上每个正确解决的组合子集额外奖励180个适应度点。因此，每个正确解码的地址总共获得200个适应度点，最大适应度为1600。其思想是让算法一次解码一个地址。事实上，个体学会先解码一个地址，然后是另一个，直到最后一个（参见图17）。

为了解决这个问题，使用了由27个基因组成的多基因染色体，每个基因只包含一个终端。因此，没有使用函数来生成图17。表2第5列（11-多路复用器）总结的实验中，运行1的群体平均适应度和最佳个体适应度的进展。

尽管子ET通过IF进行翻译后连接，但染色体没有使用函数生成。

每次运行使用的参数如表2第5列所示。本实验中，第一个正确解在运行1的第390代被发现（字符3个3个连接，形成一个深度为4的ET，由40个节点组成，前14个节点是IF，其余节点是染色体字符；参见K-表达式（3.12）和图5）：

3652bb5bbba4c87c43bcca62a51

这是一个11-多路复用器的通用解。图17显示了表2第5列总结的实验中，运行1的群体平均适应度和最佳个体适应度的进展。

如表2第五列所示，GEP以0.57的成功率解决了11-多路复用器。值得注意的是，GP在500个种群大小下，51代未能解决11-多路复用器[18]，并且只能使用4,000个个体才能解决[9]。

7. 结论
###布尔11-多路复用器 ###基因表达式编程 (GEP) ###适应度评估 ###多基因染色体 ###遗传算法 ###随机抽样 ###深度学习 ###算法优化 ###成功率 ###实验数据
&&&&
ich is a universal solution for the 11-multiplexer. Figure 17 shows the progression of average fitness of the population and the fitness of the best individual for run 1 of the experiment summarized in Table 2, column 5.

As shown in the fifth column of Table 2, GEP solves the 11-multiplexer with a success rate of 0.57. It is worth noting that GP could not solve the 11-multiplexer with a population size 500 for 51 generations [18], and could only solve it using 4,000 individuals [9].

7. Conclusions
The details of implementation of gene expression programming were thoroughly explained allowing other researchers to implement this new algorithm. Furthermore, the problems chosen to illustrate the functioning of GEP show that the new paradigm can be used to solve several problems from different fields with the advantage of running efficiently in a personal computer. The new concept behind the linear chromosomes and the ETs enabled GEP to considerably outperform existing adaptive algorithms. Therefore, GEP offers new possibilities for solving more complex technological and scientific problems. Also important and original is the multigenic organization of GEP chromosomes, which makes GEP a truly hierarchical discovery technique. And finally, gene expression algorithms represent nature more faithfully, and therefore can be used as computer models of natural evolutionary processes.

Acknowledgments
I am very grateful to José Simas for helping with hardware problems, for reading and commenting on the manuscript, and for his enthusiasm and support while I was grasping the basic ideas and concepts of GEP.

References
1. M. Mitchell, An Introduction to Genetic Algorithms (MIT Press, 1996).
2. J. Maynard Smith and E. Szathmáry, The Major Transitions in Evolution (W. H. Freeman, 1995).
3. R. Dawkins, River out of Eden (Weidenfeld and Nicolson, 1995).
4. W. Banzhaf, “Genotype-phenotype-mapping and Neutral variation - A Case Study in Genetic Programming”, in Y. Davidor, H.-P. Schwefel, and R. Männer, eds., Parallel Problem Solving from Nature III, Vol. 866 of Lecture Notes in Computer Science (Springer-Verlag, 1994).
5. R. E. Keller and W. Banzhaf, “Genetic Programming Using Genotype-phenotype Mapping from Linear Genomes into Linear Phenotypes”, in J. R. Koza, D. E. Goldberg, D. B. Fogel, and R. L. Riolo, eds., Genetic Programming 1996: Proceedings of the First Annual Conference (MIT Press, 1996).
6. M. J. Keith and M. C. Martin, “Genetic Programming in C++: Implementation Issues”, in K. E. Kinnear, ed., Advances in Genetic Programming (MIT Press, 1994).
7. W. Banzhaf, P. Nordin, R. E. Keller, and F. D. Francone, Genetic Programming: An Introduction: On the Automatic Evolution of Computer Programs and its Applications (Morgan Kaufmann, San Francisco, 1998).
8. J. H. Holland, Adaptation in Natural and Artificial Sys
###基因表达编程 ###GEP ###遗传算法 ###Genetic Programming ###11-multiplexer ###适应性算法 ###计算机模型 ###进化过程 ###线性染色体 ###多基因组织
&&&&
6. M. J. Keith and M. C. Martin, “Genetic Programming in C++: Implementation Issues”, in K. E. Kinnear, ed., Advances in Genetic Programming (MIT Press, 1994).
7. W. Banzhaf, P. Nordin, R. E. Keller, and F. D. Francone, Genetic Programming: An Introduction: On the Automatic Evolution of Computer Programs and its Applications (Morgan Kaufmann, San Francisco, 1998).
8. J. H. Holland, Adaptation in Natural and Artificial Systems: An Introductory Analysis with Applications to Biology, Control, and Artificial Intelligence, second edition (MIT Press, 1992).
9. J. R. Koza, Genetic Programming: On the Programming of Computers by Means of Natural Selection, (MIT Press, Cambridge, MA, 1992).
10. D. E. Goldberg, Genetic Algorithms in Search, Optimization, and Machine Learning (Addison-Wesley, 1989).
11. M. Lynch and J. S. Conery, “The Evolutionary Fate and Consequences of Duplicated Genes”, Science, 290 (2000), 1151-1155.
12. M. Mitchell, P. T. Hraber, and J. P. Crutchfield, “Revisiting the Edge of Chaos: Evolving Cellular Automata to Perform Computations”, Complex Systems, 7 (1993), 89-130.
13. M. Mitchell, J. P. Crutchfield, and P. T. Hraber, “Evolving Cellular Automata to Perform Computations: Mechanisms and Impediments”, Physica D, 75 (1994), 361-391.
14. J. P. Crutchfield and M. Mitchell, “The Evolution of Emergent Computation”, Proceedings of the National Academy of Sciences, USA, 82 (1995), 10742-10746.
15. R. Das, M. Mitchell, and J. P. Crutchfield, “A Genetic Algorithm Discovers Particle-based Computation in Cellular Automata”, in Y. Davidor, H.-P. Schwefel, and R. Männer, eds., Parallel Problem Solving from Nature - PPSN III (Springer-Verlag, 1994).
16. J. R. Koza, F. H. Bennett III, D. Andre, and M. A. Keane, Genetic Programming III: Darwinian Invention and Problem Solving (Morgan Kaufmann, San Francisco, 1999).
17. H. Juillé, and J. B. Pollack, “Coevolving the “Ideal” Trainer: Application to the Discovery of Cellular Automata Rules”, in J. R. Koza, W. Banzhaf, K. Chellapilla, M. Dorigo, D. B. Fogel, M. H. Garzon, D. E. Goldberg, H. Iba, and R. L. Riolo, eds., Genetic Programming 1998: Proceedings of the Third Annual Conference (Morgan Kaufmann, San Francisco, 1998).
18. U.-M. O’Reilly and F. Oppacher, “A Comparative Analysis of Genetic Programming”, in P. J. Angeline and K. E. Kinnear, eds., Advances in Genetic Programming 2 (MIT Press, 1996).
###遗传编程 ###遗传算法 ###细胞自动机 ###机器学习 ###人工智能 ###自然选择 ###进化计算 ###并行问题求解 ###计算机程序 ###旧金山 ###剑桥 ###MIT出版社