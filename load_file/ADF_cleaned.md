Automatically Defined Functions in Gene Expression Programming
Cândida Ferreira
Gepsoft, 73 Elmtree Drive, Bristol BS13 8NA, United Kingdom
candidaf@gepsoft.com, http://www.gene-expression-programming.com/gep/author.asp

In this chapter it is shown how Automatically Defined Functions are encoded in the genotype/phenotype system of Gene Expression Programming. As an introduction, the fundamental differences between Gene Expression Programming and its predecessors, Genetic Algorithms and Genetic Programming, are briefly summarized so that the evolutionary advantages of Gene Expression Programming are better understood. The introduction proceeds with a detailed description of the architecture of the main players of Gene Expression Programming (chromosomes and expression trees), focusing mainly on the interactions between them and how the simple, yet revolutionary, structure of the chromosomes allows the efficient, unconstrained exploration of the search space. The work proceeds with an introduction to Automatically Defined Functions and how they are implemented in Gene Expression Programming. Furthermore, the importance of Automatically Defined Functions in Evolutionary Computation is thoroughly analyzed by comparing the performance of sophisticated learning systems with Automatically Defined Functions with much simpler ones on the sextic polynomial problem.

2.1 Genetic Algorithms: Historical Background
The way nature solves problems and creates complexity has inspired scientists to create artificial systems that learn how to solve a particular problem without human intervention. The first attempts were done in the 1950s by Friedberg [9, 10], but ever since highly sophisticated systems have been developed that apply Darwin’s ideas of natural evolution to the artificial world of computers and modeling. Of particular interest to this work are the Genetic Algorithms (GAs) and the Genetic Programming (GP) technique as they are C. Ferreira: Automatically Defined Functions in Gene Expression Programming, Studies in Computational Intelligence (SCI) 13, 21–56 (2006) www.springerlink.com © Springer-Verlag Berlin Heidelberg 2006
22 Cândida Ferreira
the predecessors of Gene Expression Programming (GEP), an extremely versatile genotype/phenotype system. The way Automatically Defined Functions (ADFs) are implemented in GEP is another example of the great versatility of this algorithm and the versatility of GEP ADFs opens up new grounds for the creation of even more sophisticated artificial learning systems. So let’s start by introducing briefly these three techniques in order to appreciate the versatility of the genotype/phenotype system of Gene Expression Programming with and without ADFs.

2.1.1 Genetic Algorithms
Genetic Algorithms were invented by John Holland in the 1960s and they also apply biological evolution theory to computer systems [11]. And like all evolutionary computer systems, GAs are an oversimplification of biological
###Gene Expression Programming (GEP) ###Automatically Defined Functions (ADFs) ###Genetic Algorithms (GAs) ###Genetic Programming (GP) ###Evolutionary Computation ###Genotype/Phenotype System ###Artificial Learning Systems ###Search Space ###Bristol ###United Kingdom
&&&&
creation of even more sophisticated artificial learning systems. So let’s start by introducing briefly these three techniques in order to appreciate the versatility of the genotype/phenotype system of Gene Expression Programming with and without ADFs.

2.1.1 Genetic Algorithms
Genetic Algorithms were invented by John Holland in the 1960s and they also apply biological evolution theory to computer systems [11]. And like all evolutionary computer systems, GAs are an oversimplification of biological evolution. In this case, solutions to a problem are usually encoded in fixed-length strings of 0’s and 1’s (chromosomes), and populations of such strings (individuals or candidate solutions) are manipulated in order to evolve a good solution to a particular problem. From generation to generation individuals are reproduced with modification and selected according to fitness. Modification in the original genetic algorithm was introduced by the search operators of mutation, crossover, and inversion, but more recent applications started favoring mutation and crossover, dropping inversion in the process.
It is worth pointing out that GAs’ individuals consist of naked chromosomes or, in other words, GAs’ individuals are simple replicators. And like all simple replicators, the chromosomes of GAs work both as genotype and phenotype. This means that they are simultaneously the objects of selection and the guardians of the genetic information that must be replicated and passed on with modification to the next generation. Consequently, the whole structure of the replicator determines the functionality and, consequently, the fitness of the individual. For instance, in such systems it is not possible to use only a particular region of the replicator as a solution to a problem; the whole replicator is always the solution: nothing more, nothing less.

2.1.2 Genetic Programming
Genetic Programming, invented by Cramer in 1985 [1] and further developed by Koza [14], finds an alternative to fixed length solutions through the introduction of nonlinear structures (parse trees) with different sizes and shapes. The alphabet used to create these structures is also more varied than the 0’s and 1’s of GAs’ individuals, creating a richer, more versatile system of representation. Notwithstanding, GP individuals also lack a simple, autonomous genome: like the linear chromosomes of GAs, the nonlinear structures of GP are also naked replicators cursed with the dual role of genotype/phenotype.
It is worth noticing that the parse trees of GP resemble protein molecules in their use of a richer alphabet and in their complex and unique hierarchical representation. Indeed, parse trees are capable of exhibiting a great variety of functionalities. The problem with these complex replicators is that their reproduction with modification is highly constrained in evolutionary terms, simply because the modifications must take place on the parse tree itself and,
###基因表达编程 ###遗传算法 ###遗传编程 ###人工学习系统 ###生物进化理论 ###染色体 ###基因型 ###表型 ###复制子 ###变异 ###交叉 ###反转 ###解析树
&&&&
It's worth noticing that the parse trees of GP resemble protein molecules in their use of a richer alphabet and in their complex and unique hierarchical representation. Indeed, parse trees are capable of exhibiting a great variety of functionalities. The problem with these complex replicators is that their reproduction with modification is highly constrained in evolutionary terms, simply because the modifications must take place on the parse tree itself and, consequently, only a limited range of modification is possible. Indeed, the genetic operators of GP operate at the tree level, modifying or exchanging particular branches between trees.

Although at first sight this might appear advantageous, it greatly limits the GP technique (we all know the limits of grafting and pruning in nature). Consider, for instance, crossover, the most used and often the only search operator used in GP (Figure 2.1). In this case, selected branches are exchanged between two parent trees to create offspring. The idea behind its implementation was to exchange smaller, mathematically concise blocks in order to evolve more complex, hierarchical solutions composed of simpler building blocks, guaranteeing, at the same time, the creation of syntactically correct structures.

The mutation operator in GP is also very different from natural point mutation. This operator selects a node in the parse tree and replaces the branch underneath by a new randomly generated branch (Figure 2.2). Notice that the overall shape of the tree is not greatly changed by this kind of mutation, especially if lower nodes are preferentially chosen as mutation targets.

Permutation is the third operator used in Genetic Programming and the most conservative of the three. During permutation, the arguments of a randomly chosen function are randomly permuted (Figure 2.3). In this case the overall shape of the tree remains unchanged.

In summary, in Genetic Programming the operators resemble more of a conscious mathematician than the blind way of nature. But in adaptive systems the blind way of nature is much more efficient and systems such as GP are highly limited in evolutionary terms. For instance, the implementation of other operators in GP, such as the simple yet high-performing point mutation [6], is unproductive as most mutations would have resulted in syntactically incorrect structures (Figure 2.4). Obviously, the implementation of other op-
###Genetic Programming ###Parse Trees ###Genetic Operators ###Crossover ###Mutation ###Permutation ###Evolutionary Computation ###Adaptive Systems ###Syntactically Correct Structures ###Building Blocks
&&&&
conscious mathematician than the blind way of nature. But in adaptive systems the blind way of nature is much more efficient and systems such as GP are highly limited in evolutionary terms. For instance, the implementation of other operators in GP, such as the simple yet high-performing point mutation [6], is unproductive as most mutations would have resulted in syntactically incorrect structures (Figure 2.4). Obviously, the implementation of other operators such as transposition or inversion raises similar difficulties and the search space in GP remains vastly unexplored.

Fig. 2.4. Illustration of a hypothetical event of point mutation in Genetic Programming. The arrow indicates the mutation point. Note that the daughter tree is an invalid structure.

Although Koza described these three genetic operators as the basic GP operators, crossover is practically the only search operator used in most GP applications [13, 14, 15]. Consequently, no new genetic material is introduced in the genetic pool of GP populations. Not surprisingly, huge populations of parse trees must be used in order to prime the initial population with all the necessary building blocks so that good solutions could be discovered by just moving these initial building blocks around.

Finally, due to the dual role of the parse trees (genotype and phenotype), Genetic Programming is also incapable of a simple, rudimentary expression; in all cases, the entire parse tree is the solution: nothing more, nothing less.

2.1.3 Gene Expression Programming

Gene Expression Programming was invented by myself in 1999 [3], and incorporates both the simple, linear chromosomes of fixed length similar to the ones used in Genetic Algorithms and the ramified structures of different sizes and shapes similar to the parse trees of Genetic Programming. And since the ramified structures of different sizes and shapes are totally encoded in the linear chromosomes of fixed length, this is equivalent to say that, in GEP, the genotype and phenotype are finally separated from one another and the system can now benefit from all the evolutionary advantages this brings about. Thus, the phenotype of GEP consists of the same kind of ramified structure used in GP. But the ramified structures evolved by GEP (called expression trees) are the expression of a totally autonomous genome. Therefore, with GEP, a remarkable thing happened: the second evolutionary threshold – the phenotype threshold – was crossed [2]. And this means that only the genome (slightly modified) is passed on to the next generation. Consequently, one no longer needs to replicate and mutate rather cumbersome structures as all the modifications take place in a simple linear structure which only later will grow into an expression tree.

The fundamental steps of Gene Expression Programming are schematically represented in Figure 2.5. The process begins with the random generation of
###Genetic Programming ###Gene Expression Programming ###Evolutionary Algorithms ###Point Mutation ###Crossover ###Genotype ###Phenotype ###Expression Trees ###Genetic Operators ###Search Space
&&&&
The fundamental steps of Gene Expression Programming are schematically represented in Figure 2.5. The process begins with the random generation of the chromosomes of a certain number of individuals (the initial population). Then these chromosomes are expressed and the fitness of each individual is evaluated against a set of fitness cases (also called selection environment). The individuals are then selected according to their fitness (their performance in that particular environment) to reproduce with modification, leaving progeny with new traits. These new individuals are, in their turn, subjected to the same developmental process: expression of the genomes, confrontation of the selection environment, selection according to fitness, and reproduction with modification. The process is repeated for a certain number of generations or until a good solution has been found.

So, the pivotal insight of Gene Expression Programming consisted in the invention of chromosomes capable of representing any parse tree. For that purpose a new language – Karva language – was created in order to read and express the information encoded in the chromosomes. The details of this new language are given in the next section.

Furthermore, the structure of the chromosomes was designed in order to allow the creation of multiple genes, each coding for a smaller program or sub-expression tree. It is worth emphasizing that Gene Expression Programming is the only genetic algorithm with multiple genes. Indeed, in truly functional genotype/phenotype systems, the creation of more complex individuals composed of multiple genes is a child’s play, and illustrates quite well the great versatility of the GEP system. In fact, after their inception, these systems seem to catapult themselves into higher levels of complexity such as the uni- and multicellular systems, where different cells put together different combinations of genes [4]. We will see later in this chapter how the cellular system of GEP is an extremely elegant way of implementing Automatically Defined Functions that may be reused by the created programs.

The basis for all this novelty resides on the simple, yet revolutionary structure of GEP genes. This structure not only allows the encoding of any conceivable program but also allows an efficient evolution. This versatile structural organization also allows the implementation of a very powerful set of genetic operators which can then very efficiently search the solution space. As in nature, the search operators of GEP always generate valid structures and therefore are remarkably suited to creating genetic diversity.
###Gene Expression Programming ###基因表达编程 ###Chromosomes ###染色体 ###Fitness ###适应度 ###Genetic Algorithm ###遗传算法 ###Karva Language ###Karva语言 ###Multiple Genes ###多基因 ###Genotype/Phenotype Systems ###基因型/表现型系统 ###Automatically Defined Functions ###自动定义函数 ###Genetic Operators ###遗传算子 ###Solution Space ###解空间
&&&&
novelty resides on the simple, yet revolutionary structure of GEP genes. This structure not only allows the encoding of any conceivable program but also allows an efficient evolution. This versatile structural organization also allows the implementation of a very powerful set of genetic operators which can then very efficiently search the solution space. As in nature, the search operators of GEP always generate valid structures and therefore are remarkably suited to creating genetic diversity.

2 Automatically Defined Functions in GEP 27
Fig. 2.5. The flowchart of Gene Expression Programming.

2.2 The Architecture of GEP Individuals
We know already that the main players in Gene Expression Programming are the chromosomes and the expression trees (ETs), and that the latter are the expression of the genetic information encoded in the former. As in nature, the process of information decoding is called translation. And this translation implies obviously a kind of code and a set of rules. The genetic code is very simple: a one-to-one relationship between the symbols of the chromosome and the nodes they represent in the trees. The rules are also very simple: they determine the spatial organization of nodes in the expression trees and the type of interaction between sub-ETs. Therefore, there are two languages in GEP: the language of the genes and the language of expression trees and, thanks to the simple rules that determine the structure of ETs and their interactions, we will see that it is possible to infer immediately the phenotype given the sequence of a gene, and vice versa. This means that we can choose to have a very complex program represented by its compact genome without losing any information. This unequivocal bilingual notation is called Karva language. Its details are explained in the remainder of this section.

2.2.1 Open Reading Frames and Genes
The structural organization of GEP genes is better understood in terms of open reading frames (ORFs). In biology, an ORF or coding sequence of a gene begins with the start codon, continues with the amino acid codons, and ends at a termination codon. However, a gene is more than the respective ORF, with sequences upstream of the start codon and sequences downstream of the stop codon. Although in GEP the start site is always the first position of a gene, the termination point does not always coincide with the last position of a gene. Consequently, it is common for GEP genes to have noncoding regions downstream of the termination point. (For now we will not consider these noncoding regions, as they do not interfere with expression.)

Consider, for example, the algebraic expression:
√a+b / c−d (2.1)
It can also be represented as a diagram or ET:
where “Q” represents the square root function.

This kind of diagram representation is in fact the phenotype of GEP chromosomes. And the genotype can be easily inferred from the phenotype as follows:
01234567
/Q-+cdab (2.2)
###Gene Expression Programming (GEP) ###GEP genes ###Expression Trees (ETs) ###Genetic Operators ###Solution Space ###Genetic Diversity ###Karva Language ###Open Reading Frames (ORFs) ###Phenotype ###Genotype
&&&&
Consider, for example, the algebraic expression:
√
a+b
c−d(2.1)
It can also be represented as a diagram or ET:
where “Q” represents the square root function.
This kind of diagram representation is in fact the phenotype of GEP chromosomes. And the genotype can be easily inferred from the phenotype as follows:
01234567
/Q-+cdab(2.2)
which is the straightforward reading of the ET from left to right and from top to bottom (exactly as one reads a page of text). The expression (2.2) is an open reading frame, starting at “/” (position 0) and terminating at “b”(position 7). These ORFs were named K-expressions from Karva language.
Consider another ORF, the following K-expression:
2 Automatically Deﬁned Functions in GEP 29
0123456789
*//aQ*bddc(2.3)
Its expression as an ET is also very simple and straightforward. In order to express the ORF correctly, we must follow the rules governing the spatial distribution of functions and terminals. First, the start of a gene corresponds to the root of the expression tree, and it occupies the topmost position (or ﬁrst line) on the tree. Second, in the next line, below each function, are placed as many branch nodes as there are arguments to that function. Third, from left to right, the nodes are ﬁlled consecutively with the next elements of the K-expression. Fourth, the process is repeated until a line containing only terminals is formed. In this case, the expression tree is formed:
Looking at the structure of ORFs only, it is diﬃcult or even impossible to see the advantages of such a representation, except perhaps for its simplicity and elegance. However, when open reading frames are analyzed in the context of a gene, the advantages of this representation become obvious. As I said before, GEP chromosomes have ﬁxed length, and they are composed of one or more genes of equal length. Consequently, the length of a gene is also ﬁxed. Thus, in GEP, what changes is not the length of genes, but rather the length of the ORF. Indeed, the length of an ORF may be equal to or less than the length of the gene. In the ﬁrst case, the termination point coincides with the end of the gene, and in the latter, the termination point is somewhere upstream of the end of the gene. And this obviously means that GEP genes have, most of the times, noncoding regions at their ends.
And what is the function of these noncoding regions at the end of GEP genes? We will see that they are the essence of GEP and evolvability, because they allow the modiﬁcation of the genome using all kinds of genetic operators without any kind of restriction, always producing syntactically correct programs. Thus, in GEP, the fundamental property of genotype/phenotype systems – syntactic closure – is intrinsic, allowing the totally unconstrained
###GEP ###基因表达编程 ###表达式树 ###开放阅读框 ###K-表达式 ###基因型 ###表型 ###非编码区 ###遗传算子 ###语法闭包
&&&&
大多数情况下，非编码区域位于其末端。
那么，GEP基因末端的这些非编码区域有什么功能呢？我们将看到，它们是GEP和可进化性的本质，因为它们允许在没有任何限制的情况下，使用各种遗传算子修改基因组，并且总是产生语法正确的程序。因此，在GEP中，基因型/表型系统的基本属性——语法闭合——是内在的，允许基因型完全不受限制地重组，从而实现高效进化。
在下一节中，我们将分析GEP基因的结构组织，以了解它们如何始终编码语法正确的程序，以及为什么它们允许不受限制地应用几乎任何遗传算子。

2.2.2 基因的结构组织
GEP基因的新颖性在于它们由头部和尾部组成。头部包含代表函数和终端的符号，而尾部只包含终端。对于每个问题，头部的长度h是选定的，而尾部的长度t是h和具有最多参数的函数（也称为最大元数）的参数数量n的函数，并通过以下方程计算：
t = h(n-1) + 1 (2.4)
考虑一个基因，其终端集T={a, b}，函数集F={Q, *, /, -, +}，因此n=2。如果我们选择头部长度h=10，那么t=10(2-1)+1=11，基因g的长度为10+11=21。这样一个基因如下所示（尾部已加下划线）：
012345678901234567890
+*/a-Qbb/*aabaabbabaa (2.5)
它编码以下表达式树：

请注意，在这种情况下，开放阅读框在位置13结束，而基因在位置20结束。
假设现在在位置3发生了一个突变，将“a”变为“+”。那么得到以下基因：
012345678901234567890
+*/+ -Qbb/*aabaabbabaa (2.6)
其表达式给出：

在这种情况下，终止点向右移动两个位置（位置15），扩大并显著改变了子树。
显然，相反的情况也可能发生，子树可能会缩小。例如，再次考虑上面的基因（2.5），假设在位置2发生了一个突变，将“/”变为“b”：
012345678901234567890
+*b a-Qbb/*aabaabbabaa (2.7)
现在其表达式结果为以下ET：

在这种情况下，ORF在位置7结束，将原始ET缩短了六个节点。
因此，尽管基因表达编程的基因长度固定，但它们有潜力编码不同大小和形状的表达式树，其中最简单的是只包含一个节点（当基因的第一个元素是终端时），最大的是包含与基因长度相同数量的节点（当头部所有元素都是具有最大元数的函数时）。
###基因表达编程 (GEP) ###基因型/表型系统 ###语法闭合 ###遗传算子 ###基因结构 ###头部 ###尾部 ###表达式树 ###突变 ###可进化性
&&&&
In this case, the ORF ends at position 7, shortening the original ET by six nodes.
So, despite their fixed length, the genes of Gene Expression Programming have the potential to code for expression trees of different sizes and shapes, where the simplest is composed of only one node (when the first element of a gene is a terminal) and the largest is composed of as many nodes as the length of the gene (when all the elements of the head are functions with maximum arity).
It is evident from the examples above, that any modification made in the genome, no matter how profound, always results in a structurally correct program. Consequently, the implementation of a powerful set of search operators, such as point mutation, inversion, transposition, and recombination, is a child’s play, making Gene Expression Programming the ideal playground for the discovery of the perfect solution using an economy of resources (see [3] and [7] for a detailed description of the mechanisms and effects of the different genetic operators commonly used in Gene Expression Programming).

2.2.3 Multigenic Chromosomes and Linking Functions
The chromosomes of Gene Expression Programming are usually composed of more than one gene of equal length. For each problem or run, the number of genes, as well as the length of the head, are a priori chosen. Each gene codes for a sub-ET and, in problems with just one output, the sub-ETs interact with one another forming a more complex multi-subunit ET; in problems with multiple outputs, though, each sub-ET evolves its respective output.
Consider, for example, the following chromosome with length 39, composed of three genes, each with length 13 (the tails are underlined):
*Q-b/abbbaaba /aQb-bbbaabaa *Q-/b*abbbbaa (2.8)
It has three open reading frames, and each ORF codes for a sub-ET (Figure 2.6). We know already that the start of each ORF coincides with the first element of the gene and, for the sake of clarity, for each gene it is always indicated by position zero; the end of each ORF, though, is only evident upon construction of the corresponding sub-ET. As you can see in Figure 2.6, the first open reading frame ends at position 7; the second ORF ends at position 3; and the last ORF ends at position 9. Thus, GEP chromosomes contain several ORFs of different sizes, each ORF coding for a structurally and functionally unique sub-ET. Depending on the problem at hand, these sub-ETs may be selected individually according to their respective outputs, or they may form a more complex, multi-subunit expression tree and be selected as a whole. In these multi-subunit structures, individual sub-ETs interact with one another by a particular kind of posttranslational interaction or linking. For instance, algebraic sub-ETs can be linked by addition or subtraction whereas Boolean sub-ETs can be linked by OR or AND.
###Gene Expression Programming (GEP) ###Expression Trees (ET) ###Open Reading Frame (ORF) ###Multigenic Chromosomes ###Linking Functions ###Genetic Operators ###Sub-ET ###Genome Modification ###Search Operators ###Multi-subunit Structures
&&&&
unique sub-ET. Depending on the problem at hand, these sub-ETs may be selected individually according to their respective outputs, or they may form a more complex, multi-subunit expression tree and be selected as a whole. In these multi-subunit structures, individual sub-ETs interact with one another by a particular kind of posttranslational interaction or linking. For instance, algebraic sub-ETs can be linked by addition or subtraction whereas Boolean sub-ETs can be linked by OR or AND.

The linking of three sub-ETs by addition is illustrated in Figure 2.6, c. Note that the final ET could be linearly encoded as the following K-expression:
++**/Q-Q-aQ/b*b/ababbbbb (2.9)

However, the use of multigenic chromosomes is more appropriate to evolve good solutions to complex problems, for they permit the modular construction of complex, hierarchical structures, where each gene codes for a smaller and simpler building block. These building blocks are physically separated from one another, and thus can evolve independently. Not surprisingly, these multigenic systems are much more efficient than unigenic ones [3, 4]. And, of course, they also open up new grounds to solve problems of multiple outputs, such as parameter optimization or classification problems [4].

2 Automatically Defined Functions in GEP 33
Fig. 2.6. Expression of GEP genes as sub-ETs. a)A three-genic chromosome with the tails shown in bold. Position zero marks the start of each gene. b)The sub-ETs codified by each gene. c)The result of posttranslational linking with addition. The linking functions are shown in gray.

2.3 Chromosome Domains and Random Numerical Constants
We have already met two different domains in GEP genes: the head and the tail. And now another one – the Dc domain – will be introduced. This domain was especially designed to handle random numerical constants and consists of an extremely elegant, efficient, and original way of dealing with them.

As an example, Genetic Programming handles random constants by using a special terminal named “ephemeral random constant” [14]. For each ephemeral random constant used in the trees of the initial population, a random number of a special data type in a specified range is generated. Then these random constants are moved around from tree to tree by the crossover operator. Note, however, that with this method no new constants are created during evolution.

Gene Expression Programming handles random numerical constants differently [3]. GEP uses an extra terminal “?” and an extra domain Dc composed of the symbols chosen to represent the random constants. The values of each random constant, though, are only assigned during gene expression. Thus, for each gene, the initial random constants are generated during the creation of the initial population and kept in an array. However, a special operator is used to introduce genetic variation in the available pool of random constants.
###Gene Expression Programming (GEP) ###Sub-ETs ###Multigenic Chromosomes ###Posttranslational Interaction ###Random Numerical Constants ###Chromosome Domains ###Genetic Variation ###Parameter Optimization ###Classification Problems ###Ephemeral Random Constant
&&&&
GEP（Gene Expression Programming）在处理随机数值常数时有所不同。GEP使用一个额外的终端“?”和一个由代表随机常数的符号组成的额外域Dc。然而，每个随机常数的值只在基因表达期间被分配。因此，对于每个基因，初始随机常数在初始种群创建期间生成并保存在一个数组中。此外，通过直接突变随机常数，使用一个特殊的操作符在可用的随机常数池中引入遗传变异。GEP的常规操作符（突变、倒位、转座和重组），加上Dc特有的转座和Dc特有的倒位，保证了随机常数在种群中的有效循环。实际上，通过这种常数操作方案，在运行开始时生成了适当的数值常数多样性，并通过遗传操作符轻松地维护。

结构上，Dc位于尾部之后，长度等于t，由用于表示随机常数的符号组成。因此，在基因中创建了另一个具有明确边界和其自身字母表的区域。

考虑一个h=8的单基因染色体（Dc已下划线）：
01234567890123456789012345
*-Q*Q*?+?ba?babba238024198
(2.10)
其中终端“?”代表随机常数。这种染色体的表达方式与之前完全相同。然后，表达式树中的“?”从左到右、从上到下被Dc中的符号（为简单起见，用数字表示）替换。

与这些符号对应的随机常数保存在一个数组中，为简单起见，数字表示其在数组中的顺序。例如，对于以下包含10个元素的数组：
A={1.095, 1.816, 2.399, 1.618, 0.725, 1.997, 0.094, 2.998, 2.826, 2.057 }
上述染色体(2.10)给出：

这种域不仅在符号回归中，而且在参数优化和多项式归纳中都得到了极大的应用。这种优雅的结构还可以用于进化神经网络的权重和阈值，以及编码带有数值属性的决策树（未发表材料）。我们将首次看到，这种域也可以用于创建带有随机数值常数的自动定义函数（ADFs）。

自动定义函数（ADFs）首次由Koza引入，作为遗传编程中代码重用的一种方式。GP中的ADFs遵循严格的语法，其中一个S-表达式，根部有一个LIST-n函数，列出了n-1个函数定义分支和一个。
###Gene Expression Programming (GEP) ###随机数值常数 ###遗传变异 ###遗传操作符 ###自动定义函数 (ADFs) ###符号回归 ###参数优化 ###神经网络 ###决策树 ###遗传编程

**说明：**

*   **清洗：**
    *   删除了页眉页脚（如“2 Automatically Deﬁned Functions in GEP 35”、“36 Cˆ andida Ferreira”）。
    *   修正了“diﬀer-ently”为“differently”，“Dc-speciﬁc”为“Dc-specific”，“eﬀective”为“effective”，“Structurally ###the Dc comes after the tail ###has a length equal to t ###a n di s composed”修正为“结构上，Dc位于尾部之后，长度等于t，由用于表示随机常数的符号组成。”（原文此处存在排版错误和不连贯）。
    *   删除了HTML标签和多余空白。
    *   将原文中分散的段落进行了逻辑合并，使其更连贯。
    *   保留了所有重要的技术术语、数据（如数组A的数值）和公式引用（如(2.10)）。
    *   将“Automatically Deﬁned Functions”统一为“自动定义函数（ADFs）”并保持英文缩写。

*   **关键词提取：**
    *   **经营模式/产业类型：** 文本主要描述一种计算模型和技术，不直接涉及经营模式或产业类型。
    *   **技术应用：** Gene Expression Programming (GEP) ###随机数值常数 ###遗传变异 ###遗传操作符 ###自动定义函数 (ADFs) ###符号回归 ###参数优化 ###神经网络 ###决策树 ###遗传编程。这些都是文本中明确提及的技术概念和应用领域。
    *   **政策措施：** 文本不涉及政策措施。
    *   **专业术语和地理标识：** 优先提取了GEP、ADFs、遗传编程、符号回归、神经网络等专业术语。没有地理标识。
    *   **数量：** 提取了10个关键词，符合8-12个的要求。
&&&&
And we will see here for the first time that this kind of domain can also be used to create Automatically Defined Functions with random numerical constants.

2.4 Cells and the Creation of Automatically Defined Functions
Automatically Defined Functions were for the first time introduced by Koza as a way of reusing code in Genetic Programming [14]. The ADFs of GP obey a rigid syntax in which an S-expression, with a LIST-n function on the root, lists n-1 function-defining branches and one value-returning branch (Figure 2.7). The function-defining branches are used to create ADFs that may or may not be called upon by the value-returning branch. Such rigid structure imposes great constraints on the genetic operators as the different branches of the LIST function are not allowed to exchange genetic material amongst themselves. Furthermore, the ADFs of Genetic Programming are further constrained by the number of arguments each takes, as the number of arguments must be a priori defined and cannot be changed during evolution.

Fig. 2.7. The overall structure of an S-expression with two function-defining branches and the value-returning branch used in Genetic Programming to create Automatically Defined Functions.

In the multigenic system of Gene Expression Programming, the implementation of Automatically Defined Functions can be done elegantly and without any kind of constraints as each gene is used to encode a different ADF [4]. The way these ADFs interact with one another and how often they are called upon is encoded in special genes – homeotic genes – thus called because they are the ones controlling the overall development of the individual. And continuing with the biological analogy, the product of expression of such genes is also called a cell. Thus, homeotic genes determine which genes are expressed in which cell and how they interact with one another. Or stated differently, homeotic genes determine which ADFs are called upon in which main program and how they interact with one another. How this is done is explained in the remainder of this section.

2.4.1 Homeotic Genes and the Cellular System of GEP
Homeotic genes have exactly the same kind of structure as conventional genes and are built using an identical process. They also contain a head and a tail domain, with the heads containing, in this case, linking functions (so called because they are actually used to link different ADFs) and a special class of terminals – genic terminals – representing conventional genes, which, in the cellular system, encode different ADFs; the tails contain obviously only genic terminals.

Consider, for instance, the following chromosome:
01234567801234567801234567801234567890
/-b/abbaa*a-/abbab-*+abbbaa**Q2+010102
(2.11)
It codes for three conventional genes and one homeotic gene (underlined).
###Automatically Defined Functions ###Genetic Programming ###Gene Expression Programming ###S-expression ###Homeotic Genes ###Cellular System ###Genic Terminals ###Evolution ###Code Reuse ###Multigenic System
&&&&
ning, in this case, linking functions (so called because they are actually used to link different ADFs) and a special class of terminals – genic terminals – representing conventional genes, which, in the cellular system, encode different ADFs; the tails contain obviously only genic terminals.

Consider, for instance, the following chromosome:
01234567801234567801234567801234567890
/-b/abbaa*a-/abbab-*+abbbaa**Q2+010102
(2.11)
It codes for three conventional genes and one homeotic gene (underlined). The conventional genes encode, as usual, three different sub-ETs, with the difference that now these sub-ETs will act as ADFs and, therefore, may be invoked multiple times from different places. And the homeotic gene controls the interactions between the different ADFs (Figure 2.8). As you can see in Figure 2.8, in this particular case, ADF 0 is used twice in the main program, whereas ADF 1 and ADF 2 are both used just once.

It is worth pointing out that homeotic genes have their specific length and their specific set of functions. And these functions can take any number of arguments (functions with one, two, three, ..., n, arguments). For instance, in the particular case of chromosome (2.11), the head length of the homeotic gene hH is equal to five, whereas for the conventional genes h= 4; the function set used in the homeotic gene FH consists of FH={+, -, *, /, Q }, whereas for the conventional genes the function set consists of F={+, -, *, / }. As shown in Figure 2.8, this cellular system is not only a form of elegantly allowing the evolution of linking functions in multigenic systems but also an extremely elegant way of encoding ADFs that can be called an arbitrary number of times from an arbitrary number of different places.

2.4.2 Multicellular Systems
The use of more than one homeotic gene results obviously in a multicellular system, in which each homeotic gene puts together a different consortium of genes.

Consider, for instance, the following chromosome:
38 Cˆ andida Ferreira
012345601234560123456012345678012345678
*Q-bbabQ*baabb-/abbab*+21Q1102/*21+1011
(2.12)
It codes for three conventional genes and two homeotic genes (underlined). And its expression results in two different cells or programs, each expressing different genes in different ways (Figure 2.9). As you can see in Figure 2.9, ADF 1 is used twice in both cells; ADF 2 is used just once in both cells; and ADF 0 is only used in Cell 1.

The applications of these multicellular systems are multiple and varied and, like the multigenic systems, they can be used both in problems with just one output and in problems with multiple outputs. In the former case, the best program or cell accounts for the fitness of the individual; in the latter, each cell is responsible for a particular facet in a multiple output task such as a classification task with multiple classes.

Fig. 2.8. Expression of a unicellular system with three Automatically Defined Functions.
###基因组学 ###遗传算法 ###自动定义函数 (ADF) ###同源基因 ###多细胞系统 ###单细胞系统 ###基因编码 ###基因表达 ###多基因系统 ###染色体
&&&&
ations of these multicellular systems are multiple and varied and, like the multigenic systems, they can be used both in problems with just one output and in problems with multiple outputs. In the former case, the best program or cell accounts for the ﬁtness of the individual; in the latter, each cell is responsible for a particular facet in a multiple output task such as a classiﬁcation task with multiple classes.

Fig. 2.8. Expression of a unicellular system with three Automatically Deﬁned Functions. a) The chromosome composed of three conventional genes and one homeotic gene (shown in bold). b) The ADFs codiﬁed by each conventional gene. c) The main program or cell.

2 Automatically Deﬁned Functions in GEP 39

Fig. 2.9. Expression of a multicellular system with three Automatically Deﬁned Functions. a) The chromosome composed of three conventional genes and two homeotic genes (shown in bold). b) The ADFs codiﬁed by each conventional gene. c) Two diﬀerent main programs expressed in two diﬀerent cells. Note how diﬀerent cells put together diﬀerent combinations of ADFs.

It is worth pointing out that the implementation of multiple main programs in Genetic Programming is virtually unthinkable and so far no one has attempted it.

2.4.3 Incorporating Random Numerical Constants in ADFs

The incorporation of random numerical constants in Automatically Deﬁned Functions is also easy and straightforward. As you probably guessed, the gene structure used to accomplish this includes the special domain Dc for encod-ing the random numerical constants, which, for the sake of simplicity and eﬃciency, is only implemented in the genes encoding the ADFs (one can ob-viously extend this organization to the homeotic genes, but nothing is gained from that except a considerable increase in computational eﬀort). The structure of the homeotic genes remains exactly the same and they continue to control how often each ADF is called upon and how they interact with one another.

Consider, for instance, the chromosome with two conventional genes and their respective arrays of random numerical constants:
0123456789001234567890012345678012345678
**?b?aa4701+/Q?ba?8536*0Q-10010/Q-+01111(2.13)
A0={0.664, 1.703, 1.958, 1.178, 1.258, 2.903, 2.677, 1.761, 0.923, 0.796 }
A1={0.588, 2.114, 0.510, 2.359, 1.355, 0.186, 0.070, 2.620, 2.374, 1.710 }

The genes encoding the ADFs are expressed exactly as normal genes with a Dc domain and, therefore, their respective ADFs will, most probably, include random numerical constants (Figure 2.10). Then these ADFs with random numerical constants are called upon as many times as necessary from any of the main programs encoded in the homeotic genes. As you can see in Figure 2.10, ADF0 is invoked twice in Cell 0 and once in Cell 1, whereas ADF1 is used just once in Cell 0 and called three diﬀerent times in Cell 1.

2.5 Analyzing the Importance of ADFs in Automatic Programming
###自动定义函数 (ADFs) ###基因表达式编程 (GEP) ###多细胞系统 ###单细胞系统 ###染色体 ###基因 ###同源基因 ###随机数值常数 ###自动编程 ###计算效率
&&&&
Dc domain and, therefore, their respective ADFs will, most probably, include random numerical constants (Figure 2.10). Then these ADFs with random numerical constants are called upon as many times as necessary from any of the main programs encoded in the homeotic genes. As you can see in Figure 2.10, ADF 0 is invoked twice in Cell 0 and once in Cell 1, whereas ADF 1 is used just once in Cell 0 and called three different times in Cell 1.

2.5 Analyzing the Importance of ADFs in Automatic Programming
The motivation behind the implementation of Automatically Defined Functions in Genetic Programming, was the belief that ADFs allow the evolution of modular solutions and, consequently, improve the performance of the GP technique [13, 14, 15]. Koza proved this by solving a sextic polynomial problem and the even-parity functions, both with and without ADFs [15].

In this section, we are going to solve the sextic polynomial problem using not only a cellular system with ADFs but also a multigenic system with static linking and a simple unigenic system. The study of the simple unigenic system is particularly interesting because it has some similarities with the GP system without ADFs.

2.5.1 General Settings
The sextic polynomial of this section x^6 - 2x^4 + x^2 was chosen by Koza [15] because of its potentially exploitable regularity and modularity, easily guessed by its factorization:
x^6 - 2x^4 + x^2 = x^2 (x - 1)^2 (x + 1)^2 (2.14)

For this problem, the basic parameters common to both GEP and GP, irrespective of the presence or absence of ADFs, were kept exactly the same as those used by Koza. Thus, a set of 50 random fitness cases chosen from the interval [-1.0, +1.0] was used; and a very simple function set, composed only of the four arithmetic operators F={+, -, *, / }was used. As for random numerical constants, we will see that their use in this problem is not crucial for the evolution of perfect solutions. Nonetheless, evolution still goes smoothly if integer constants are used and, therefore, one can illustrate the role random constants play and how they are integrated in Automatically Defined Functions by choosing integer random constants. So, when used, integer random constants are chosen from the interval [0, 3].

Fig. 2.10. Expression of a multicellular system with Automatically Defined Functions containing random numerical constants. a) The chromosome composed of three conventional genes and two homeotic genes (shown in bold). b) The ADFs codified by each conventional gene. c) Two different programs expressed in two different cells.

The fitness function used to evaluate the performance of each evolved program is based on the relative error and explores the idea of a selection range and a precision. The selection range is used as a limit for selection to operate, above which the performance of a program on a particular fitness case.
###Automatically Defined Functions (ADFs) ###Genetic Programming (GP) ###Gene Expression Programming (GEP) ###经营模式 ###模块化解决方案 ###蜂窝系统 ###多基因系统 ###单基因系统 ###六次多项式问题 ###适应度函数 ###随机数值常数 ###遗传算法
&&&&
They are integrated in Automatically Defined Functions by choosing integer random constants. So, when used, integer random constants are chosen from the interval [0, 3].

The fitness function used to evaluate the performance of each evolved program is based on the relative error and explores the idea of a selection range and a precision. The selection range is used as a limit for selection to operate, above which the performance of a program on a particular fitness case contributes nothing to its fitness. And the precision is the limit for improvement, as it allows the fine-tuning of the evolved solutions as accurately as necessary.

Mathematically, the fitness $f_i$ of an individual program $i$ is expressed by the equation:
$f_i = n / \sum_{j=1} ( | P(i,j) - T_j | / T_j \cdot 100 )$ (2.15)
where $R$ is the selection range, $P(i,j)$ the value predicted by the individual program $i$ for fitness case $j$ (out of $n$ fitness cases) and $T_j$ is the target value for fitness case $j$. Note that the absolute value term corresponds to the relative error. This term is what is called the precision and if the error is lower than or equal to the precision then the error becomes zero. Thus, for a perfect fit, the absolute value term is zero and $f_i = f_{max} = nR$. In all the experiments of this work we are going to use a selection range of 100 and a precision of 0.01, thus giving for the set of 50 fitness cases $f_{max} = 5,000$. It is worth pointing out that these conditions, especially the precision of 0.01, guarantee that all perfect solutions are indeed perfect and match exactly the target function (2.14). This is important to keep in mind since the performance of the different systems will be compared in terms of success rate.

2.5.2 Results without ADFs
The importance of Automatically Defined Functions and the advantages they bring to Evolutionary Computation can only be understood if one analyzes their behavior and how the algorithm copes with their integration. Is evolution still smooth? Are there gains in performance? Is the system still simple or excessively complicated? How does it compare to simpler systems without ADFs? How does one integrate random numerical constants in ADFs? Are these ADFs still manageable or excessively complex? Are there problems that can only be solved with ADFs? These are some of the questions that we will try to address in this work. And for that we are going to start this study by analyzing two simpler systems: the simpler of the two is the unigenic system of GEP that evolves a single parse tree and therefore bares some resemblance to the GP system without ADFs; the other one is the multigenic system of GEP that evolves multiple parse trees linked together by a predefined linking function.

The Unigenic System
For this analysis, we are going to use the basic Gene Expression Algorithm.
###Automatically Defined Functions (ADFs) ###Evolutionary Computation ###Fitness Function ###Relative Error ###Selection Range ###Precision ###Gene Expression Programming (GEP) ###Unigenic System ###Multigenic System ###Parse Tree
&&&&
本文旨在探讨两种基因表达编程（GEP）系统：单基因系统和多基因系统。单基因GEP系统演化单个解析树，与不带ADF（自动定义函数）的GP（遗传编程）系统相似。多基因GEP系统则演化多个解析树，并通过预定义的连接函数连接。

**单基因系统**
本分析将使用基本的基因表达算法，分别测试带随机常数和不带随机常数的情况。两种情况下，都将演化一个编码在单个基因中的树结构。

实验参数如表2.1所示。值得注意的是，本次实验中使用的种群规模较小，仅为50个个体，远小于Koza [15] 解决相同问题时使用的4,000个个体。本研究中，50个个体的种群规模保持不变，以便更好地比较不同系统。此外，在可能的情况下，本研究中使用的最大程序大小约为50个点，以便在所有实验之间进行比较。具体来说，对于单基因系统，头部长度为24时最大程序大小为49；对于具有四个基因且头部长度为六的多基因系统，最大程序大小为52。因此，本研究中的单基因系统选择了头部长度h=24的染色体，最大程序长度为49（请注意，带随机数值常数的系统由于Dc域的存在，染色体长度会更长）。

如表2.1所示，使用不带随机数值常数的单基因系统解决此问题的成功率（26%）远高于使用ugGEP-RNC算法的成功率（4%）。这再次表明，对于这种简单的、模块化的系统，不带随机常数的单基因系统表现更优。

**表2.1. 使用单基因系统（ugGEP）和带随机数值常数的单基因系统（ugGEP-RNC）解决六次多项式问题的设置**

| 参数                       | ugGEP | ugGEP-RNC |
| :------------------------- | :---- | :-------- |
| 运行次数                   | 100   | 100       |
| 代数                       | 200   | 200       |
| 种群规模                   | 50    | 50        |
| 染色体长度                 | 49    | 74        |
| 基因数量                   | 1     | 1         |
| 头部长度                   | 24    | 24        |
| 基因长度                   | 49    | 74        |
| 终端集                     | aa    | aa        |
| 函数集                     | +-*/  | +-*/      |
| 突变率                     | 0.044 | 0.044     |
| 反转率                     | 0.1   | 0.1       |
| RIS转座率                  | 0.1   | 0.1       |
| IS转座率                   | 0.1   | 0.1       |
| 两点重组率                 | 0.3   | 0.3       |
| 单点重组率                 | 0.3   | 0.3       |
| 每基因随机常数             | –     | 5         |
| 随机常数数据类型           | –     | 整数      |
| 随机常数范围               | –     | 0 - 3     |
| Dc特异性突变率             | –     | 0.044     |
| Dc特异性反转率             | –     | 0.1       |
| Dc特异性IS转座率           | –     | 0.1       |
| 随机常数突变率             | –     | 0.01      |
| 适应度案例数               | 50    | 50        |
| 选择范围                   | 100   | 100       |
| 精度                       | 0.01  | 0.01      |
| 成功率                     | 26%   | 4%        |
###基因表达编程 ###GEP ###单基因系统 ###多基因系统 ###遗传编程 ###GP ###自动定义函数 ###ADF ###解析树 ###随机常数 ###种群规模 ###染色体长度 ###六次多项式问题 ###成功率 ###实验参数
&&&&
constants per gene –5
Random constants data type – Integer
Random constants range –0 - 3
Dc-specific mutation rate – 0.044
Dc-specific inversion rate –0 . 1
Dc-specific IS transposition rate –0 . 1
Random constants mutation rate –0 . 0 1
Number of fitness cases 50 50
Selection range 100 100
Precision 0.01 0.01
Success rate 26% 4%
Candida Ferreira
than the success rate obtained with the ugGEP-RNC algorithm (26% as opposed to just 4%), which, again, shows that, for this kind of simple, modular problem, evolutionary algorithms fare far better if the numerical constants are created from scratch by the algorithm itself through the evolution of simple mathematical expressions. This is not to say that, for complex real-world problems of just one variable or really complex problems of higher dimensions, random numerical constants are not important; indeed, most of the times, they play a crucial role in the discovery of good solutions.
Let’s take a look at the structure of the first perfect solution found using the unigenic system without the facility for the manipulation of random numerical constants:
*++a/****+-a--*/aa*/*---aaaaaaaaaaaaaaaaaaaaaaaaa(2.16)
As its expression shows, it contains a relatively big neutral region involving a total of nine nodes and two smaller ones involving just three nodes each. It is also worth pointing out the creation of the numerical constant one through the simple arithmetic operation a/a.
It is also interesting to take a look at the structure of the first perfect solution found using the unigenic system with the facility for the manipulation of random numerical constants:
*a+*aa+*a*/aa-a*++-?aa*a?aaa???aaaaaa?a?...
...a?a???a?a0210121021334303442030040
A={1, 1, 1, 1, 3 }(2.17)
As its expression reveals, it is a fairly compact solution with no obvious neutral regions that makes good use of the random numerical constant one to evolve a perfect solution.
The Multigenic System with Static Linking
For this analysis we are going to use again both the basic Gene Expression Algorithm without random constants and GEP with random numerical constants. The parameters and the performance of both experiments are shown in Table 2.2.
It is worth pointing out that maximum program length in these experiments is similar to the one used in the unigenic systems of the previous section. Here, head lengths h= 6 and four genes per chromosome were used, giving maximum program length of 52 points (again note that the chromosome length in the systems with random numerical constants is larger on account of the Dc domain, but maximum program length remains the same).
Automatically Defined Functions in GEP
Table 2.2. Settings for the sextic polynomial problem using a multigenic system with ( mgGEP-RNC ) and without ( mgGEP ) random numerical constants
mgGEP mgGEP-RNC
Number of runs 100 100
###进化算法 ###基因表达编程 (GEP) ###随机数值常数 (RNC) ###单基因系统 ###多基因系统 ###变异率 ###反转率 ###转座率 ###适应度函数 ###成功率 ###模块化问题 ###数学表达式
&&&&
h=6，每个染色体有四个基因，最大程序长度为52点（请注意，在带有随机数值常数的系统中，由于Dc域的存在，染色体长度更大，但最大程序长度保持不变）。
2 GEP中自动定义函数 45
表2.2。使用多基因系统（mgGEP-RNC）和不使用（mgGEP）随机数值常数进行六次多项式问题的设置
mgGEP mgGEP-RNC
运行次数 100 100
代数 200 200
种群大小 50 50
染色体长度 52 80
基因数量 44
头部长度 66
基因长度 13 20
连接函数 **
终端集 aa ?
函数集 +-*/ +-*/
突变率 0.044 0.044
倒位率 0.1 0.1
RIS转座率 0.1 0.1
IS转座率 0.1 0.1
两点重组率 0.3 0.3
单点重组率 0.3 0.3
基因重组率 0.3 0.3
基因转座率 0.1 0.1
每个基因的随机常数 –5
随机常数数据类型 – 整型
随机常数范围 –0 - 3
Dc特异性突变率 – 0.044
Dc特异性倒位率 –0.1
Dc特异性IS转座率 –0.1
随机常数突变率 –0.01
适应度案例数 50 50
选择范围 100 100
精度 0.01 0.01
成功率 93% 49%
通过比较表2.1和2.2可以看出，多基因的使用显著提高了两个系统的性能。在没有随机数值常数的系统中，通过将基因组划分为四个自主基因，性能从26%提高到93%；而在有随机数值常数的系统中，性能从4%提高到49%。另请注意，在此分析中，当引入随机数值常数时，观察到熟悉的模式：成功率从93%显著下降到49%（在单基因系统中，从26%下降到4%）。
我们再来看看使用多基因系统（不具备随机数值常数操作功能）找到的第一个完美解的结构（子ET通过乘法连接）：
46 Cândida Ferreira
0123456789012012345678901201234567890120123456789012
+/aaa/aaaaaaa+//a/aaaaaaaa-**a/aaaaaaaa-**a/aaaaaaaa(2.18)
正如其表达式所示，它包含三个小的中性区域，共涉及九个节点，所有节点都编码数值常数一。另请注意，在两次（在子ET 0和1中），数值常数一在完美解的整体形成中起着重要作用。关于这个完美解的另一个有趣之处是，基因2和基因3完全相同，这表明发生了重大的基因复制事件（值得指出的是，基因复制只能通过基因重组和基因转座的协同作用来实现，因为基因复制操作符不属于基因表达编程的遗传修饰工具）。
###基因表达编程 ###多基因系统 ###随机数值常数 ###基因重组 ###基因转座 ###基因复制 ###成功率 ###突变率 ###倒位率 ###适应度 ###染色体 ###种群大小
&&&&
and 1), the numerical constant one plays an important role in the overall making of the perfect solution. Also interesting about this perfect solution, is that genes 2 and 3 are exactly the same, suggesting a major event of gene duplication (it’s worth pointing out that the duplication of genes can only be achieved by the concerting action of gene recombination and gene transposition, as a gene duplication operator is not part of the genetic modification arsenal of Gene Expression Programming). It is also interesting to take a look at the structure of the first perfect solution found using the multigenic system with the facility for the manipulation of random numerical constants (the sub-ETs are linked by multiplication):
01234567890123456789
+--+*aa??aa?a0444212+--+*aa??aa?a0244422
a?a??a?aaa?a?2212021
aa-a*/?aa????3202123
A
0={0, 3, 1, 2, 1 }
A1={0, 3, 1, 2, 1 }
A2={0, 3, 1, 2, 1 }
A3={3, 3, 2, 0, 2 }(2.19)
As its expression reveals, it is a fairly compact solution with two small neutral motifs plus a couple of neutral nodes, all representing the numerical constant zero. Note that genes 0 and 1 are almost exact copies of one another (there is only variation at positions 17 and 18, but they are of no consequence as they are part of a noncoding region of the gene), suggesting a recent event of gene duplication. Note also that although genes 2 and 3 encode exactly the same sub-ET (a simple sub-ET with just one node), they most certainly followed different evolutionary paths as the homology between their sequences suggests.

2.5.3 Results with ADFs
In this section, we are going to conduct a series of four studies, each with four different experiments. In the first study, we are going to use a unicellular system encoding 1, 2, 3, and 4 ADFs. In the second study, we are going to use again a unicellular system, encoding also 1, 2, 3, and 4 ADFs, but, in this case, the ADFs will also incorporate random numerical constants. The third and fourth studies are respectively similar to the first and second one, with the difference that we are going to use a system with multiple cells (three, to be precise) instead of just the one.

2 Automatically Defined Functions in GEP 47
The Unicellular System
For the unicellular system without random numerical constants, both the parameters and performance are shown in Table 2.3. It is worth pointing out, that, in these experiments, we are dealing with Automatically Defined Functions that can be reused again and again, and therefore it makes little sense to talk about maximum program length. However, in these series of experiments the same head length of six was used to encode all the ADFs and a system with four ADFs was also analyzed, thus allowing the comparison of these cellular systems with the simpler acellular ones (recall that we used four genes with h= 6 in the multigenic system and one gene with h=2 4i nt h e unigenic system).
As you can see in Table 2.3, these cellular systems with Automatically
###基因表达编程 ###基因复制 ###基因重组 ###基因转座 ###多基因系统 ###自动定义函数 ###单细胞系统 ###数值常数 ###进化路径 ###非编码区
&&&&
因此，谈论最大程序长度意义不大。然而，在这些系列实验中，所有ADF都使用相同的六个头部长度进行编码，并且还分析了一个具有四个ADF的系统，从而允许将这些细胞系统与更简单的无细胞系统进行比较（回想一下，我们在多基因系统中使用了四个基因，h=6，在单基因系统中使用了h=24）。

如表2.3所示，这些具有自动定义功能的细胞系统表现出色，特别是与单基因系统（参见表2.1）相比，后者是我们能最接近遗传编程系统的。因此，我们也可以得出结论，ADF的使用可以为仅限于一个基因或解析树的系统带来可观的收益，尤其是在手头的问题具有一定模块性时。然而，请注意，单细胞系统与具有静态链接的多基因系统（参见表2.2）相比略显逊色，这表明GEP的多基因系统已经是一个高效的系统，可以用于解决几乎任何类型的问题。

值得指出的是，Koza [15] 在分析ADF解决此问题的作用时，只使用了一个ADF，如表2.3所示，这是解决此问题最成功的组织方式，成功率为82%。而且，奇怪的是，在所有此处进行的实验中都出现了相同的模式，即当只使用一个ADF时获得了最高的成功率（参见表2.3、2.4、2.5和2.6）。

让我们看一下使用单细胞系统编码一个ADF所找到的第一个完美解决方案的结构：
0123456789012012345678
-a**aaaaaaaaa*/0*00000(2.20)
正如其表达式所示，主程序远非简洁，可以简化为(ADF)²。但尽管如此，它完美地说明了进化过程本身创建的有用构建块如何被编码在同源基因中的主程序多次重用。

我们还分析了一个具有多个ADF的程序的结构，下面是一个具有四个ADF的个体（基因单独显示）：
0123456789012
*-a--+aaaaaaa
/-a---aaaaaaa-a*+*-aaaaaaa
a+*-+aaaaaaaa
*22121133(2.21)
48 Cândida Ferreira
正如其表达式所示，主程序相当紧凑，只调用了ADF 2。所有其余的ADF都没有被使用，因此可以自由进化而没有太大压力。我们已经知道中性区域在自然进化 [12] 和GEP [5] 中都扮演着重要角色，并且它们的适当使用是性能显著提高的原因。在这些细胞系统中也观察到相同的现象，其中最简单的系统，只有一个ADF和一个单细胞，似乎拥有适量的中性区域，因为它以82%的成功率高效进化。
###自动定义功能 (ADF) ###遗传编程 (GP) ###多基因系统 ###单基因系统 ###细胞系统 ###无细胞系统 ###中性区域 ###进化过程 ###成功率 ###模块性
&&&&
We know already that neutral regions play an important role both in natural evolution [12] and in GEP [5], and that their use in good measure is responsible for a considerable increase in performance. And the same phenomenon is observed in these cellular systems, where the simplest one with only one ADF and a single cell seems to have the right amount of neutral regions as it evolves very efficiently with a success rate of 82%. So, in this particular problem, by increasing the number of ADFs, we are basically increasing the number of neutral regions, and the performance for this simple modular problem decreases proportionately, dropping down to 63% in the system with four ADFs (see Table 2.3).

Table 2.3. Settings and performance for the sextic polynomial problem using a unicellular system encoding 1, 2, 3, and 4 ADFs
| Setting/ADF Count | 1 ADF | 2 ADFs | 3 ADFs | 4 ADFs |
|---|---|---|---|---|
| Number of runs | 100 | 100 | 100 | 100 |
| Number of generations | 200 | 200 | 200 | 200 |
| Population size | 50 | 50 | 50 | 50 |
| Chromosome length | 22 | 35 | 48 | 61 |
| Number of genes/ADFs | 1 | 2 | 3 | 4 |
| Head length | 6 | 6 | 6 | 6 |
| Gene length | 13 | 13 | 13 | 13 |
| Function set of ADFs | +-*/ | +-*/ | +-*/ | +-*/ |
| Terminal set | a | aaa | | |
| Number of homeotic genes/cells | 1 | 1 | 1 | 1 |
| Head length of homeotic genes | 4 | 4 | 4 | 4 |
| Length of homeotic genes | 9 | 9 | 9 | 9 |
| Function set of homeotic genes | +-*/ | +-*/ | +-*/ | +-*/ |
| Terminal set of homeotic genes | ADF 0 | ADFs 0-1 | ADFs 0-2 | ADFs 0-3 |
| Mutation rate | 0.044 | 0.044 | 0.044 | 0.044 |
| Inversion rate | 0.1 | 0.1 | 0.1 | 0.1 |
| RIS transposition rate | 0.1 | 0.1 | 0.1 | 0.1 |
| IS transposition rate | 0.1 | 0.1 | 0.1 | 0.1 |
| Two-point recombination rate | 0.3 | 0.3 | 0.3 | 0.3 |
| One-point recombination rate | 0.3 | 0.3 | 0.3 | 0.3 |
| Gene recombination rate | 0.3 | 0.3 | 0.3 | 0.3 |
| Gene transposition rate | – | 0.1 | 0.1 | 0.1 |
| Mutation rate in homeotic genes | 0.044 | 0.044 | 0.044 | 0.044 |
| Inversion rate in homeotic genes | 0.1 | 0.1 | 0.1 | 0.1 |
| RIS transp. in homeotic genes | 0.1 | 0.1 | 0.1 | 0.1 |
| IS transp. in homeotic genes | 0.1 | 0.1 | 0.1 | 0.1 |
| Number of fitness cases | 50 | 50 | 50 | 50 |
| Selection range | 100 | 100 | 100 | 100 |
| Precision | 0.01 | 0.01 | 0.01 | 0.01 |
| Success rate | 82% | 78% | 69% | 63% |

2 Automatically Defined Functions in GEP 49
Let’s now analyze the behavior of the unicellular system when random numerical constants are also incorporated in the Automatically Defined Functions. For that purpose a similar set of experiments were done, using also 1, 2, 3, and 4 ADFs (Table 2.4). And as expected, a considerable decrease in performance was observed comparatively to the performance observed in the unicellular system without random numerical constants (see Table 2.3).

Let’s take a look at the structure of the first perfect solution found using the unicellular system encoding just one ADF with random constants:
01234567890123456789012345678
---*a-?aa?a??0412201*+0*00000
A={1, 0, 3, 1, 2 }(2.22)
As its expression shows, the simple module discovered in the structure encoding the ADF (a2-1) is called four times in the main program, creating a perfect solution with just one kind of building block.
###基因表达编程 (GEP) ###自动定义函数 (ADF) ###中性区域 ###蜂窝系统 ###成功率 ###遗传算法参数 ###随机数值常数 ###模块化问题 ###基因重组 ###突变率 ###单细胞系统 ###六次多项式问题
&&&&
Let’s take a look at the structure of the first perfect solution found using the unicellular system encoding just one ADF with random constants:
01234567890123456789012345678
---*a-?aa?a??0412201*+0*00000
A={1, 0, 3, 1, 2 }(2.22)
As its expression shows, the simple module discovered in the structure encoding the ADF (a^2-1) is called four times in the main program, creating a perfect solution with just one kind of building block.

Let’s now analyze the structure of a program with more than one ADF, the individual below with four ADFs with random numerical constants (the genes are shown separately):
01234567890123456789
*-+*a*?aaa?a?3324010
-aa?*-aa?a???3123440
*a/a-a?aa?a??2234201--*+*+??aa?aa0141122
*00003233
A0={1, 1, 2, 1, 1 }
A1={2, 3, 0, 2, 0 }
A2={3, 1, 0, 0, 3 }
A3={2, 0, 3, 2, 2 }(2.23)
As its expression reveals, the main program is fairly compact and invokes only ADF 0. Indeed, for this simple modular problem, most perfect solutions involve just one ADF, suggesting that this problem is better solved using just one kind of building block that can then be used as many times as necessary by the main program. And the fact that the system evolves more efficiently with just one ADF is just another indication of this (57% success rate in the system with just one ADF versus 26% in the system with four ADFs).

Table 2.4. Settings and performance for the sextic polynomial problem using a unicellular system encoding 1, 2, 3, and 4 ADFs with random numerical constants
| Setting/ADF Count | 1 ADF | 2 ADFs | 3 ADFs | 4 ADFs |
|---|---|---|---|---|
| Number of runs | 100 | 100 | 100 | 100 |
| Number of generations | 200 | 200 | 200 | 200 |
| Population size | 50 | 50 | 50 | 50 |
| Chromosome length | 29 | 49 | 69 | 89 |
| Number of genes/ADFs | 1 | 2 | 3 | 4 |
| Head length | 6 | 6 | 6 | 6 |
| Gene length | 20 | 20 | 20 | 20 |
| Function set of ADFs | +-*/ | +-*/ | +-*/ | +-*/ |
| Terminal set | a? | a? | a? | a? |
| Number of homeotic genes/cells | 1 | 1 | 1 | 1 |
| Head length of homeotic genes | 4 | 4 | 4 | 4 |
| Length of homeotic genes | 9 | 9 | 9 | 9 |
| Function set of homeotic genes | +-*/ | +-*/ | +-*/ | +-*/ |
| Terminal set of homeotic genes | ADF 0 | ADFs 0-1 | ADFs 0-2 | ADFs 0-3 |
| Mutation rate | 0.044 | 0.044 | 0.044 | 0.044 |
| Inversion rate | 0.1 | 0.1 | 0.1 | 0.1 |
| RIS transposition rate | 0.1 | 0.1 | 0.1 | 0.1 |
| IS transposition rate | 0.1 | 0.1 | 0.1 | 0.1 |
| Two-point recombination rate | 0.3 | 0.3 | 0.3 | 0.3 |
| One-point recombination rate | 0.3 | 0.3 | 0.3 | 0.3 |
| Gene recombination rate | 0.3 | 0.3 | 0.3 | 0.3 |
| Gene transposition rate | – | 0.1 | 0.1 | 0.1 |
| Random constants per gene | 5 | 5 | 5 | 5 |
| Random constants data type | Integer | Integer | Integer | Integer |
| Random constants range | 0-3 | 0-3 | 0-3 | 0-3 |
| Dc-specific mutation rate | 0.044 | 0.044 | 0.044 | 0.044 |
| Dc-specific inversion rate | 0.1 | 0.1 | 0.1 | 0.1 |
| Dc-specific IS transposition rate | 0.1 | 0.1 | 0.1 | 0.1 |
| Random constants mutation rate | 0.01 | 0.01 | 0.01 | 0.01 |
| Mutation rate in homeotic genes | 0.044 | 0.044 | 0.044 | 0.044 |
| Inversion rate in homeotic genes | 0.1 | 0.1 | 0.1 | 0.1 |
| RIS transp. in homeotic genes | 0.1 | 0.1 | 0.1 | 0.1 |
| IS transp. in homeotic genes | 0.1 | 0.1 | 0.1 | 0.1 |
| Number of fitness cases | 50 | 50 | 50 | 50 |
| Selection range | 100 | 100 | 100 | 100 |
###unicellular system ###ADF (Automatically Defined Function) ###random numerical constants ###perfect solution ###building block ###modular problem ###sextic polynomial problem ###genetic programming ###mutation rate ###recombination rate ###homeotic genes ###success rate
&&&&
Random constants range 0-3 0-3 0-3 0-3
Dc-specific mutation rate 0.044 0.044 0.044 0.044
Dc-specific inversion rate 0.1 0.1 0.1 0.1
Dc-specific IS transposition rate 0.1 0.1 0.1 0.1
Random constants mutation rate 0.01 0.01 0.01 0.01
Mutation rate in homeotic genes 0.044 0.044 0.044 0.044
Inversion rate in homeotic genes 0.1 0.1 0.1 0.1
RIS transp. in homeotic genes 0.1 0.1 0.1 0.1
IS transp. in homeotic genes 0.1 0.1 0.1 0.1
Number of fitness cases 50 50 50 50
Selection range 100 100 100 100
Precision 0.01 0.01 0.01 0.01
Success rate 57% 42% 33% 26%

The Multicellular System
For the multicellular system without random numerical constants, both the parameters and performance are shown in Table 2.5.
2 Automatically Defined Functions in GEP 51
As you can see, these multicellular systems with Automatically Defined Functions perform extremely well, even better than the multigenic system with static linking (see Table 2.2). And they are very interesting because they can also be used to solve problems with multiple outputs, where each cell is engaged in the identification of one class or output. Here, however, we are using a multicellular system to solve a problem with just one output, which means that all the cells are trying to find the same kind of solution and, therefore, for each individual, the fitness is determined by the best cell. Obviously, the greater the number of cells the higher the probability of evolving the perfect solution or cell. But there is one caveat though: one cannot go on increasing the number of cells indefinitely because it takes time and resources to express all of them. The use of three cells per individual seems a good compromise.

Table 2.5. Settings and performance for the sextic polynomial problem using a multicellular system encoding 1, 2, 3, and 4 ADFs
1 ADF 2 ADFs 3 ADFs 4 ADFs
Number of runs 100 100 100 100
Number of generations 200 200 200 200
Population size 50 50 50 50
Chromosome length 40 53 66 79
Number of genes/ADFs 1 2 3 4
Head length 6 6 6 6
Gene length 13 13 13 13
Function set of ADFs +-*/ +-*/ +-*/ +-*/
Terminal set a a a a
Number of homeotic genes/cells 3 3 3 3
Head length of homeotic genes 4 4 4 4
Length of homeotic genes 9 9 9 9
Function set of homeotic genes +-*/ +-*/ +-*/ +-*/
Terminal set of homeotic genes ADF 0 ADFs 0-1 ADFs 0-2 ADFs 0-3
Mutation rate 0.044 0.044 0.044 0.044
Inversion rate 0.1 0.1 0.1 0.1
RIS transposition rate 0.1 0.1 0.1 0.1
IS transposition rate 0.1 0.1 0.1 0.1
Two-point recombination rate 0.3 0.3 0.3 0.3
One-point recombination rate 0.3 0.3 0.3 0.3
Gene recombination rate 0.3 0.3 0.3 0.3
Gene transposition rate – 0.1 0.1 0.1
Mutation rate in homeotic genes 0.044 0.044 0.044 0.044
Inversion rate in homeotic genes 0.1 0.1 0.1 0.1
RIS transp. in homeotic genes 0.1 0.1 0.1 0.1
IS transp. in homeotic genes 0.1 0.1 0.1 0.1
Number of fitness cases 50 50 50 50
Selection range 100 100 100 100
Precision 0.01 0.01 0.01 0.01
Success rate 98% 96% 95% 90%
52 Candida Ferreira
the number of cells indefinitely because it takes time and resources to express all of them. The use of three cells per individual seems a good compromise.
###Multicellular System ###Automatically Defined Functions (ADFs) ###Gene Expression Programming (GEP) ###Mutation Rate ###Inversion Rate ###Transposition Rate ###Homeotic Genes ###Sextic Polynomial Problem ###Fitness Cases ###Success Rate ###Recombination Rate ###Cell-based System
&&&&
Mutation rate in homeotic genes 0.044
Inversion rate in homeotic genes 0.1
RIS transp. in homeotic genes 0.1
IS transp. in homeotic genes 0.1
Number of fitness cases 50
Selection range 100
Precision 0.01
Success rate 98% 96% 95% 90%

Cândida Ferreira

The number of cells indefinitely because it takes time and resources to express all of them. The use of three cells per individual seems a good compromise, and we are going to use just that in all the experiments of this section.

Let’s take a look at the structure of the first perfect solution found using the multicellular system encoding just one ADF (which cell is best is indicated after the coma):
-*a*aaaaaaaaa-0-+000000***00000-**+00000,2(2.24)
As its expression shows, the best main program invokes the ADF encoded in the conventional gene five times. Note, however, that this perfect solution is far from parsimonious and could indeed be simplified to (ADF)2.

It is also interesting to take a look at what the other cells are doing. For instance, Cell 0 encodes zero and Cell 1 encodes (ADF)4, both a far cry from the perfect solution.

Let’s also analyze the structure of a program with more than one ADF, the individual below with four ADFs and three cells (the best cell is indicated after the coma):
**-/aaaaaaaaa/aaaa/aaaaaaa*-a*/aaaaaaaa/-***/aaaaaaa
*-*222301*+2021323-+0020321,1(2.25)
As its expression shows, the best main program invokes two different ADFs (ADF0 and ADF2), but since ADF0 encodes zero, the best cell could be simplified to (ADF2)2, which is again a perfect solution built with just one kind of building block (a3−a). It is also worth noticing that two of the ADFs (ADF0 and ADF3) and one of the cells (Cell 0) encode zero, and the numerical constant one is also encoded by ADF1; they are all good examples of the kind of neutral region that permeates all these solutions.

Let’s now analyze the behavior of the multicellular system when random numerical constants are also incorporated in the Automatically Defined Functions.

For that purpose a similar set of experiments were done, using also 1, 2, 3, and 4 ADFs (Table 2.6). And as expected, a considerable decrease in performance was observed comparatively to the performance obtained in the multicellular system without random numerical constants (see Table 2.5). Notwithstanding, ADFs with random numerical constants perform quite well despite the additional complexity, and they may prove valuable in problems where random numerical constants are crucial to the discovery of good solutions.

Automatically Defined Functions in GEP
Table 2.6. Settings and performance for the sextic polynomial problem using a multicellular system encoding 1, 2, 3, and 4 ADFs with random numerical constants
1ADF 2ADFs 3ADFs 4ADFs
###homeotic genes ###multicellular system ###Automatically Defined Functions (ADF) ###Gene Expression Programming (GEP) ###random numerical constants ###sextic polynomial problem ###mutation rate ###inversion rate ###fitness cases ###success rate
&&&&
ADFs with random numerical constants perform quite well despite the additional complexity, and they may prove valuable in problems where random numerical constants are crucial to the discovery of good solutions.

2 Automatically Defined Functions in GEP 53
Table 2.6. Settings and performance for the sextic polynomial problem using a multicellular system encoding 1, 2, 3, and 4 ADFs with random numerical constants

1 ADF 2 ADFs 3 ADFs 4 ADFs
Number of runs 100 100 100 100
Number of generations 200 200 200 200
Population size 50 50 50 50
Chromosome length 29 67 87 107
Number of genes/ADFs 12 3 4
Head length 66 6 6
Gene length 20 20 20 20
Function set of ADFs +-*/ +-*/ +-*/ +-*/
Terminal set a? a? a? a?
Number of homeotic genes/cells 13 3 3
Head length of homeotic genes 44 4 4
Length of homeotic genes 99 9 9
Function set of homeotic genes +-*/ +-*/ +-*/ +-*/
Terminal set of homeotic genes ADF 0 ADFs 0-1 ADFs 0-2 ADFs 0-3
Mutation rate 0.044 0.044 0.044 0.044
Inversion rate 0.1 0.1 0.1 0.1
RIS transposition rate 0.1 0.1 0.1 0.1
IS transposition rate 0.1 0.1 0.1 0.1
Two-point recombination rate 0.3 0.3 0.3 0.3
One-point recombination rate 0.3 0.3 0.3 0.3
Gene recombination rate 0.3 0.3 0.3 0.3
Gene transposition rate – 0.1 0.1 0.1
Random constants per gene 55 5 5
Random constants data type Integer Integer Integer Integer
Random constants range 0-3 0-3 0-3 0-3
Dc-specific mutation rate 0.044 0.044 0.044 0.044
Dc-specific inversion rate 0.1 0.1 0.1 0.1
Dc-specific IS transposition rate 0.1 0.1 0.1 0.1
Random constants mutation rate 0.01 0.01 0.01 0.01
Mutation rate in homeotic genes 0.044 0.044 0.044 0.044
Inversion rate in homeotic genes 0.1 0.1 0.1 0.1
RIS transp. in homeotic genes 0.1 0.1 0.1 0.1
IS transp. in homeotic genes 0.1 0.1 0.1 0.1
Number of fitness cases 50 50 50 50
Selection range 100 100 100 100
Precision 0.01 0.01 0.01 0.01
Success rate 79% 60% 58% 50%

Let’s take a look at the structure of a perfect solution found using the multicellular system encoding just one ADF with random numerical constants (the best cell is indicated after the coma):
-***a?aaa???a4000424+/0+00000*0*/00000-+*-00000,1
A={3, 1, 1, 1, 1 }(2.26)
As its expression shows, the main program encoded in Cell 1 is far from parsimonious, but it encodes nonetheless a perfect solution to the sextic polynomial (2.14). The only available ADF is called four times from the main program, but in essence it could have been called just twice as it can be simplified to (ADF)2.

Let’s now analyze the structure of a program with more than one ADF, the individual below with four ADFs and three cells (the best cell is indicated after the coma):
-a*-*a?aa????2322013?-*//aaa?aa?a2412442
*a+a*aa?aaaaa4024010
*-a?a?aaa????3224232
A0={0, 0, 0, 1, 0 }
A1={2, 0, 0, 2, 2 }
A2={2, 1, 3, 0, 0 }
A3={2, 1, 3, 0, 0 }
###自动定义函数（ADF） ###基因表达式编程（GEP） ###随机数值常数 ###多细胞系统 ###六次多项式问题 ###基因 ###染色体长度 ###变异率 ###重组率 ###成功率 ###适应度案例 ###精确度
&&&&
Let’s now analyze the structure of a program with more than one ADF, the individual below with four ADFs and three cells (the best cell is indicated after the coma):
-a*-*a?aa????2322013?-*//aaa?aa?a2412442
*a+a*aa?aaaaa4024010
*-a?a?aaa????3224232
A
0={0, 0, 0, 1, 0 }
A1={2, 0, 0, 2, 2 }
A2={2, 1, 3, 0, 0 }
A3={2, 1, 3, 0, 0 }
*2*/00213/-+*03022233201102,0(2.27)
As its expression shows, the best main program invokes two different ADFs (ADF 0 and ADF 2), but the calls to ADF 2 cancel themselves out, and the main program is reduced to (ADF 0)2, which, of course is a perfect solution to the problem at hand.

2.6 Summary
Comparatively to Genetic Programming, the implementation of Automatically Defined Functions in Gene Expression Programming is very simple because it stands on the shoulders of the multigenic system with static linking and, therefore, requires just a small addition to make it work. And because the cellular system of GEP with ADFs, like all GEP systems, continues to be totally encoded in a simple linear genome, it poses no constraints whatsoever to the action of the genetic operators and, therefore, these systems can also evolve efficiently (indeed, all the genetic operators of GEP were easily extended to the homeotic genes). As a comparison, the implementation of ADFs in GP adds additional constraints to the already constrained genetic operators in order to ensure the integrity of the different structural branches of the parse tree. Furthermore, due to its mammothness, the implementation of multiple main programs in Genetic Programming is prohibitive, whereas in GEP the creation of a multicellular system encoding multiple main programs is a child’s play.

Indeed, another advantage of the cellular system of GEP, is that it can easily grow into a multicellular one, encoding not just one but multiple cells or main programs, each using a different set of ADFs. These multicellular systems have multiple applications, some of which were already illustrated in this work, but their real potential resides in solving problems with multiple outputs where each cell encodes a program involved in the identification of a certain class or pattern. Indeed, the high performance exhibited by the multicellular system in this work gives hope that this system can be fruitfully explored to solve much more complex problems. In fact, in this work, not only the multicellular but also the unicellular and the multigenic system with static linking, were all far from stretched to their limits as the small population sizes of just 50 individuals used in all the experiments of this work indicate. As a comparison, to solve this same problem, the GP system with ADFs uses already populations of 4,000 individuals.
###Automatically Defined Functions (ADF) ###Gene Expression Programming (GEP) ###Genetic Programming (GP) ###Multicellular System ###Multigenic System ###Static Linking ###Genetic Operators ###Linear Genome ###Parse Tree ###Problem Solving
&&&&
lar system in this work gives hope that this system can be fruitfully explored to solve much more complex problems. In fact, in this work, not only the multicellular but also the unicellular and the multigenic system with static linking, were all far from stretched to their limits as the small population sizes of just 50 individuals used in all the experiments of this work indicate. As a comparison, to solve this same problem, the GP system with ADFs uses already populations of 4,000 individuals.

And yet another advantage of the ADFs of Gene Expression Programming, is that they are free to become functions of one or several arguments, being this totally decided by evolution itself. Again, in GP, the number of arguments each ADF takes must be a priori decided and cannot be changed during the course of evolution lest invalid structures are created.

And finally, the cellular system (and multicellular also) encoding ADFs with random numerical constants was for the first time described in this work. Although their performance was also compared to other systems, the main goal was to show that ADFs with random numerical constants can also evolve efficiently, extending not only their appeal but also the range of their potential applications.

References
1. N.L. Cramer, A Representation for the Adaptive Generation of Simple Sequential Programs. In J. J. Grefenstette, ed., “Proceedings of the First International Conference on Genetic Algorithms and Their Applications”, Erlbaum, 1985
2. R. Dawkins, River out of Eden, Weidenfeld and Nicolson, 1995
3. C. Ferreira, Gene Expression Programming: A New Adaptive Algorithm for Solving Problems, Complex Systems, 13 (2): 87-129, 2001
4. C. Ferreira, Gene Expression Programming: Mathematical Modeling by an Artificial Intelligence, Angra do Heroísmo, Portugal, 2002
5. C. Ferreira, Genetic Representation and Genetic Neutrality in Gene Expression Programming, Advances in Complex Systems, 5 (4): 389-408, 2002
6. C. Ferreira, Mutation, Transposition, and Recombination: An Analysis of the Evolutionary Dynamics. In H.J. Caulfield, S.-H. Chen, H.-D. Cheng, R. Duro, V. Honavar, E.E. Kerre, M. Lu, M. G. Romay, T. K. Shih, D. Ventura, P.P. Wang, Y. Yang, eds., “Proceedings of the 6th Joint Conference on Information Sciences, 4th International Workshop on Frontiers in Evolutionary Algorithms”, pp. 614-617, Research Triangle Park, North Carolina, USA, 2002
7. C. Ferreira, Gene Expression Programming and the Evolution of Computer Programs. In L.N. de Castro and F.J. Von Zuben, eds., “Recent Developments in Biologically Inspired Computing”, pp. 82-103, Idea Group Publishing, 2004
8. C. Ferreira, Designing Neural Networks Using Gene Expression Programming, 9th Online World Conference on Soft Computing in Industrial Applications, September 20 - October 8, 2004
9. R.M. Friedberg, A Learning Machine: Part I, IBM Journal, 2 (1): 2-13, 1958
10. R.M. Friedberg, B. Dunham, and J.H. North, A Learning Machine: Part II, IBM
###Gene Expression Programming ###Adaptive Algorithm ###Genetic Algorithms ###Evolutionary Algorithms ###Artificial Intelligence ###Neural Networks ###Biologically Inspired Computing ###Complex Systems ###ADFs ###Angra do Heroísmo ###Research Triangle Park ###North Carolina
&&&&
8. C. Ferreira, Designing Neural Networks Using Gene Expression Programming, 9th Online World Conference on Soft Computing in Industrial Applications, September 20 - October 8, 2004
9. R.M. Friedberg, A Learning Machine: Part I, IBM Journal, 2 (1): 2-13, 1958
10. R.M. Friedberg, B. Dunham, and J.H. North, A Learning Machine: Part II, IBM Journal, 3 (7): 282-287, 1959
11. J.H. Holland, Adaptation in Natural and Artificial Systems: An Introductory Analysis with Applications to Biology, Control, and Artificial Intelligence, University of Michigan Press, USA, 1975 (second edition: MIT Press, 1992)
12. M. Kimura, The Neutral Theory of Molecular Evolution, Cambridge University Press, Cambridge, UK, 1983
13. J.R. Koza, F.H. Bennett III, D. Andre, and M.A. Keane, Genetic Programming III: Darwinian Invention and Problem Solving, Morgan Kaufmann Publishers, San Francisco, USA, 1999
14. J.R. Koza, Genetic Programming: On the Programming of Computers by Means of Natural Selection, MIT Press, Cambridge, MA, USA, 1992
15. J.R. Koza, Genetic Programming II: Automatic Discovery of Reusable Programs, MIT Press, Cambridge, MA, USA, 1994
###基因表达编程 ###神经网络 ###软计算 ###学习机器 ###人工智能 ###生物学 ###控制 ###分子进化 ###遗传编程 ###自然选择 ###美国 ###英国