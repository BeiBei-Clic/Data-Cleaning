IEEE TRANSACTIONS ON EVOLUTIONARY COMPUTATION, VOL. 20, NO. 1, FEBRUARY 2016 65
自学习基因表达式编程

Jinghui Zhong, Yew-Soon Ong, and Wentong Cai

摘要：本文提出了一种名为SL-GEP的新型自学习基因表达式编程（GEP）方法，旨在提高GEP的搜索准确性和效率。与现有GEP变体不同，SL-GEP的特点是采用了一种新颖的染色体表示，其中每个染色体都嵌入了可用于构建最终解决方案的子函数。作为染色体的一部分，这些子函数在进化搜索过程中通过所提出的算法进行自学习或自进化。通过将子函数或任何部分解决方案作为另一个子函数的输入参数，SL-GEP促进了复杂、高阶和建设性子函数的形成，从而提高了搜索的准确性和效率。此外，SL-GEP中染色体的进化还提出了一种基于差分进化的新型搜索机制。所提出的SL-GEP简单、通用，并且比传统的GEP变体具有更少的控制参数。SL-GEP在15个符号回归问题和6个偶校验问题上进行了验证。实验结果表明，所提出的SL-GEP在准确性和搜索效率方面优于几种最先进的算法。

索引词：偶校验问题，进化计算，基因表达式编程（GEP），遗传编程（GP），符号回归问题。

I. 引言
遗传编程（GP）是一种进化计算技术，已被证明可用于自动化设计解决用户定义任务的计算机程序[1]、[2]。自Koza[1]提出以来，GP的许多变体已经发展起来[3]–[6]。其中一个值得注意的变体是基因表达式编程（GEP），由Ferreira[5]引入。GEP的独特之处在于它采用了一种基因表达式表示，通过使用固定长度的字符串而不是像传统GP那样使用解析树来建模计算机程序。通过基因表达式表示，GEP被证明可以提供比GP更简洁和可读的解决方案[7]。在过去十年中，GEP已广泛应用于许多领域，包括分类问题、时间序列预测等[7]–[11]。然而，由于其迭代性质，GEP可能计算量很大，尤其是在处理大规模问题时。此外，GEP算法中包含许多控制参数，需要耗时的微调。

手稿于2014年6月13日收到；2014年12月31日修订；2015年4月5日接受。出版日期为2015年4月20日；当前版本日期为2016年1月27日。本研究由Tier 1学术研究基金项目RG23/14资助。

作者隶属于计算机工程学院。
###基因表达式编程 ###遗传编程 ###进化计算 ###自学习 ###符号回归
&&&&
计算密集型任务，尤其是在处理大规模问题时。此外，GEP算法中包含许多控制参数，需要耗时进行微调。

手稿于2014年6月13日收到；2014年12月31日修订；2015年4月5日接受。出版日期为2015年4月20日；当前版本日期为2016年1月27日。本研究由Tier 1学术研究基金项目RG23/14资助。

作者来自新加坡南洋理工大学计算机工程学院（邮编：639798）。

为了提高GP在大型复杂应用中的性能，一种有效的方法是引入高阶知识以加速搜索。例如，考虑经典的10位偶校验问题，对于传统的GP来说，仅使用“AND”、“OR”和“NOT”等基本操作符很难解决这个问题。然而，如果引入“XOR”函数作为新的基本操作符，问题的复杂性可以大大降低，从而显著加速搜索过程。但是，定义此类高阶知识通常是领域特定的，并且可能并非易事。

在GP领域，已有研究尝试自动化获取高阶知识。例如，Angeline和Pollack以及Kameya等人尝试从历史搜索信息中挖掘有前景的部分解作为高阶知识，并确保它们在进化过程中得以保留。同时，Koza将高阶知识视为自动定义函数（ADFs）的形式，并提出在进化过程中通过GP自动进化ADFs。ADFs是为特定子问题提供子解决方案的子函数。然后，ADFs可以组合起来为更大的问题提供解决方案。到目前为止，ADFs已被证明在提高GP在一系列问题上的性能方面非常有效。最近，Walker和Miller还在嵌入式笛卡尔GP（ECGP）中考虑使用ADFs，据报道，ECGP在各种问题上的表现优于GP和带有ADFs的GP。

与之前的研究相比，目前关于将ADFs等高阶知识引入GEP以增强其性能的研究很少。Ferreira曾对使用ADFs来改进GEP（命名为GEP-ADF）进行了初步研究。然而，GEP-ADF的机制使其在处理大规模复杂问题时效率低下或不可扩展。此外，GEP-ADF比传统GEP拥有更多的新操作符和控制参数，这使得其在实际使用中不便。

为了解决上述问题，本文提出了一种新颖的自学习GEP（SL-GEP）方法。在所提出的SL-GEP中，每个染色体都被设计为包含一个主结构。
###GEP ###高阶知识 ###自动定义函数 ###(ADFs) ###自学习GEP ###(SL-GEP) ###遗传编程 ###(GP)
&&&&
初步研究表明，使用ADF（自动定义函数）可以增强GEP（基因表达编程），形成GEP-ADF。然而，GEP-ADF的机制使其在处理大规模复杂问题时效率低下或不可扩展。此外，GEP-ADF比传统GEP增加了更多新操作符和控制参数，这给实际应用带来了不便。

为了解决上述问题，本文提出了一种新颖的自学习GEP（SL-GEP）方法。在所提出的SL-GEP中，每个染色体都设计为包含一个主程序和一组ADF，所有这些都使用基因表达方法表示。每个ADF都是解决子问题的子函数，并与主程序结合以解决感兴趣的给定问题。作为染色体的一部分，ADF能够自学习，因此在SL-GEP中随着进化的在线进行而自动设计。在初始化步骤中，每个染色体中编码的所有ADF都是随机生成的。然后，在每一代中，包括变异和交叉在内的进化算子将相应地进化染色体的ADF。通过选择算子，产生高质量解决方案的ADF更有可能在世代之间存活下来。通过这种方式，高质量的ADF与进化搜索过程一起进化。

SL-GEP的一个显著特点是，其ADF可以包含其他ADF和/或主程序的任何子树作为输入参数，从而形成复杂的ADF（C-ADF）。这一特点在设计复杂且具有建设性的ADF方面，比经典的GEP搜索和GEP-ADF提供了显著的灵活性，从而提高了搜索的准确性和效率。此外，本文还提出了一种基于差分进化（DE）的新型搜索机制，用于有效且高效地进化解决方案种群。所提出的SL-GEP易于实现，通用性强，并且比GEP和GEP-ADF包含更少的控制参数。在实验部分，通过15个符号回归基准和6个偶校验问题，全面验证了所提出的SL-GEP。结果表明，SL-GEP在准确性和搜索效率方面优于几种最先进的GP变体。

本文的其余部分组织如下：第二节描述了相关背景技术；第三节描述了所提出的SL-GEP；第四节介绍了实验研究；最后，第五节得出结论。
###GEP ###ADF ###SL-GEP ###基因表达编程 ###差分进化
&&&&
研究结果表明，SL-GEP在准确性和搜索效率方面优于其他几种最先进的GP变体。
本文的其余部分组织如下：第二节描述了相关的背景技术；第三节描述了所提出的SL-GEP；第四节介绍了实验研究；最后，第五节得出结论。

**二、预备知识**
本节简要介绍了本文所考虑技术的一些背景知识。
通常，GP已广泛应用于各种领域，其中最常见的应用之一是符号回归[25, 26]。因此，本文在此给出了符号回归问题的正式定义，以帮助读者更好地理解我们提出的方法。然后介绍了传统的GEP基因表达方法[5]，接着描述了结合GEP-ADF中引入的ADF的扩展基因表达方法[23]。最后，讨论了其他相关的GEP变体。

**A. 符号回归问题**
给定一组包含输入变量值和输出响应的测量数据，符号回归问题涉及寻找一个数学公式S(·)来描述输入变量与输出之间的关系。推导出的数学公式S(·)可以提供对生成数据的系统的深入了解，从而可以后续用于预测新输入变量的输出。
形式上，第i个样本数据可以表示为：
[vi,1, vi,2, ..., vi,n, oi] (1)
其中n是输入变量的数量，vi,j是第i个样本数据的第j个变量值，oi是相应的输出。
公式S(·)由函数符号（例如，+，×，和sin）、变量和常量组成。S(·)的质量通过其对给定数据的拟合精度进行评估。这通常使用均方根误差（RMSE）来实现：
f(S(·)) = √(∑(yi - oi)² / N) (2)
其中yi是S(·)对第i个输入数据的输出，oi是第i个输入数据的真实输出，N是需要拟合的数据量。因此，给定一个函数集和变量集作为构建块，解决符号回归问题的任务是找到使给定数据的RMSE最小化的最优公式S(·)*：
S(·)* = arg min S(·) f(S(·)) (3)

**B. 传统的GEP基因表达方法**
在传统的GP中，数学公式S(·)由树结构表示，该树结构包含两种类型的节点：函数节点和终端节点。函数节点有一个或多个子节点（例如，+和sin），而终端节点是没有子节点的叶节点（例如，变量和常量）。GEP不使用传统GP中的解析树，而是使用固定长度的字符串来表示数学公式。如图1所示，染色体由符号字符串表示。
###SL-GEP ###符号回归 ###基因表达编程 ###均方根误差 ###优化 ###**说明：** ###1. ###**删除无用字符 ###格式错误 ###重复内容：** ###移除了不必要的换行符 ###页眉页脚信息（如“Fig. ###1.”） ###并统一了标点符号。 ###2. ###**修正明显的错别字和语法错误：** ###* ###"thatthe" ###-> ###"that ###the" ###* ###"efﬁciency" ###-> ###"efficiency" ###(字体问题) ###* ###"P ###RELIMINARIES" ###-> ###"预备知识" ###(标题翻译并规范化) ###* ###"applicationsand" ###-> ###"applications ###and" ###* ###"compre-hending" ###-> ###"comprehending" ###(断字问题) ###* ###"thatincorporates" ###-> ###"that ###incorporates" ###* ###"radicalBigg/summationtextN ###i=1(yi−oi)2 ###N(2)" ###-> ###"√(∑(yi ###- ###oi)² ###/ ###N) ###(2)" ###(公式的正确表示) ###* ###"ﬁtting" ###-> ###"fitting" ###(字体问题) ###* ###"ﬁnding" ###-> ###"finding" ###(字体问题) ###* ###"ﬁxed-length" ###-> ###"fixed-length" ###(字体问题) ###* ###调整了句子的结构 ###使其更符合中文表达习惯 ###例如将“ts ###obtained ###demonstrate ###that ###the ###SL-GEP ###outperforms ###several ###state-of-the-art ###GP ###variants ###in ###terms ###of ###accuracy ###and ###search ###efﬁciency.”修正为“研究结果表明 ###SL-GEP在准确性和搜索效率方面优于其他几种最先进的GP变体。” ###3. ###**保持原文的核心意思和逻辑结构：** ###文本内容和段落划分与原文保持一致 ###确保了信息的完整性和逻辑连贯性。 ###4. ###**提取3-5个关键词：** ###选择了最能概括文本核心内容的关键词。
&&&&
GEP（基因表达式编程）与传统GP（遗传编程）的区别在于，传统GP使用树结构表示数学公式，包含函数节点（有子节点，如“+”和“sin”）和终端节点（叶节点，如变量和常量）。而GEP则使用固定长度的字符串来表示数学公式。

如图1所示，GEP的染色体由两部分组成：头部（Head）和尾部（Tail）。头部元素可以是函数或终端，而尾部元素只能是终端。例如，给定函数集 $\Psi_1 = \{+, -, *, /, \cos, \exp\}$ 和终端集 $\Gamma_1 = \{x, y\}$，一个长度为17的基因表达式染色体可以表示为 $X = [+, -, \cos, *, x, -, \exp, +, y, x, x, x, x, y, x, y, x]$。

每个基因表达式染色体都可以通过广度优先遍历方案转换为等效的表达式树（ET）。例如，上述染色体可以转换为图2(a)所示的ET形式，其数学表达式为 $(\exp(x) * (x+x) - x) + \cos(y-x)$。

头部（h）和尾部（l）的长度是固定的。为了确保任何染色体都能正确转换为有效的ET，h和l受到约束：$l = h \cdot (u-1) + 1$，其中u是函数中子节点的最大数量。例如，如果u=2，则 $l = h+1$。

图2展示了两个ET示例：(a)原始ET，(b)通过变异原始ET中的一个符号而修改的ET。图3展示了GEP-ADF中基因表达式染色体的结构。

需要注意的是，每个染色体的尾部可能存在冗余元素，这些元素在当前搜索代次的ET构建中未使用。然而，这些未使用的元素可能在后续的搜索演化中变得有用。例如，参考染色体(6)，如果第五个符号（即x）演变为“+”，则第14和15个元素（即y和x）将从冗余变为对构建收敛的ET有用，如图2(b)所示。此外，由于最终ET中的节点数量从未超过预定义的染色体长度，基因表达式方法倾向于生成短程序，从而避免了GP的膨胀限制。

经典的GEP进化操作包括初始化、评估、精英选择、选择、变异、反转、IS-转座、根转座、单点交叉和两点交叉。GEP的实现细节可参考[5]和[8]。

**C. GEP-ADF中使用的扩展基因表达式技术**
Ferreira [23]将ADF与GEP结合，形成了GEP-ADF。在GEP-ADF中，每个染色体包含一个数字。
###GEP ###基因表达式编程 ###表达式树 ###染色体 ###进化操作
&&&&
本文旨在避免GP（Genetic Programming）的膨胀限制。在经典的GEP（Gene Expression Programming）中，进化算子包括初始化、评估、精英选择、选择、变异、反转、IS-转座、根转座、单点交叉和两点交叉。GEP的实现细节可参考[5]和[8]。

**C. GEP-ADF中使用的扩展基因表达技术**
Ferreira [23]将ADF（Automatically Defined Functions）与GEP结合，提出了GEP-ADF。在GEP-ADF中，每个染色体由多个常规基因和一个同源基因组成，如图3所示。所有常规基因和同源基因都使用基因表达表示。每个常规基因编码一个子ET（Expression Tree），并作为ADF。同源基因通过连接函数（例如，+和*）融合不同的ADF，并编码生成最终输出的主程序。ADF的函数集和终端集与传统基因表达方法相同。另一方面，同源基因的函数集包含连接函数，而同源基因的终端集只包含ADF。

例如，考虑染色体：
[*,+,-,y,x,x,z,+,/,-,x,y,z,x,*,*,sin,2,+,1,2,1,2,1,2] (9)
图4展示了GEP-ADF的示例染色体及其对应的ET。该染色体编码了两个ADF和一个同源基因（即主程序）。GEP-ADF的示例ET如图4所示。可以看出，ADF1和ADF2在同源基因中都使用了两次。此外，需要注意的是，在这种染色体表示中，ADF只能用作同源基因的终端，并且不包含输入参数。

**D. 其他相关的GEP变体**
自GEP首次引入以来，已经提出了各种增强的GEP变体。现有工作主要集中于将新操作或自适应参数控制策略与GEP结合，以提高搜索效率。例如，Liu等人[27]提出了一种扩展GEP，它自适应地用随机生成的个体替换较差的个体，以增加种群多样性。还采用了混合选择方法来提高搜索效率。类似地，Zhang和Xiao [28]提出了一种修改的GEP，它动态地改变种群大小（NP），以避免局部停滞。Peng等人[29]提出了一种新的方法来评估基因表达染色体的适应度，而无需先构建树再遍历树进行适应度评估，据报道该方法能够减少GEP的计算量。Bautu等人[30]提出了一种自适应GEP，它自适应地调整染色体中使用的基因数量。Huang [50]研究了GEP的模式理论，并提出了一些描述模式从一代传播到另一代的定理。

与以前的工作相比，本文将规范的GEP与ADF作为染色体表示的一部分进行了扩展。
###GEP ###ADF ###基因表达 ###进化算法 ###染色体表示
&&&&
该方法被报道能够减少GEP的计算量。Bautu等人[30]提出了一种自适应GEP，它自适应地调整染色体中使用的基因数量。Huang[50]研究了GEP的图式理论，并提出了一些描述图式从一代传播到另一代的定理。

与以前的工作相比，本文扩展了经典的GEP，将ADF作为染色体表示的一部分，它们与搜索进化一起自进化或自学习，同时将其用于加速搜索。此外，本文在GEP中开发了新颖的基于DE的算子。所提出的基于DE的搜索机制不仅包含更少的控制参数，而且提供了改进的搜索性能。

III. 自学习基因表达式编程

本节描述了所提出的SL-GEP方法，它是经典GEP以及GEP-ADF的增强版本。与现有GEP方法相比，SL-GEP引入了一种新颖的染色体表示，有助于形成C-ADF，它简洁地体现了复杂和建设性的高阶知识。此外，提出了一种新颖的进化搜索机制来简化SL-GEP中染色体的进化。由于ADF和C-ADF是与GEP搜索进化一起自学习的，我们将所提出的算法标记为SL-GEP。

A. 提出的染色体表示

在所提出的SL-GEP中，每个染色体包含一个“主程序”和几个ADF，如图5所示。主程序是解决方案的压缩表达式，提供最终输出。同时，每个ADF是一个子函数，可以组合起来解决主程序中的更大问题。主程序和ADF都使用基因表达式表示。但主程序和ADF具有不同的函数集和终端集。对于主程序，函数集不仅包含函数（例如，+，-和sin），还包含染色体中定义的ADF，而终端集包含变量和常量（例如，x，y和π）。对于ADF，函数集包含函数，而终端集包含输入参数。表I比较并对比了本文考虑的三种基因表达式方法的函数集和终端集。

图6显示了SL-GEP中提出的表示的示例染色体。假设u的值为2，h和l设置为h=4和l=5；头长度（h'）
###基因表达式编程 ###自学习 ###染色体表示 ###自适应 ###进化算法
&&&&
对于ADFs（自动定义函数），函数集由函数组成，而终端集由输入参数组成。表I比较并对比了本文考虑的三种基因表达方法的函数集和终端集。

图6展示了SL-GEP中建议表示的一个染色体示例。假设（8）中的u值为2，h和l设置为：h=4，l=5；ADFs的头部长度（h'）和尾部长度（l'）分别设置为：h'=3，l'=4。

表I：三种基因表达技术中的函数集和终端集。

一个典型的包含一个ADF的染色体可以表示为：
[G, sin, G, G, x, π, x, z, y, *, +, *, a, b, a, b] (10)
其中，{+, *, sin}是函数集，G是ADF，{x, z, π}是终端集，{a, b}是输入参数集。

如图6所示，主程序可以解码为：
G(sin(G(x,z)), G(x,π)) (11)
ADF可以解码为：
G(a,b) = (a+b) * (a*b) (12)
将（12）代入（11），我们得到最终表达式（S）：
S = G(sin(G(x,z)), G(x,π))
= G(sin((x+z)*(x*z)), (x+π)*(x*π))
= (sin((x+z)*(x*z)) + (x+π)*(x*π))) * (sin((x+z)*(x*z)) * (x+π)*(x*π))) (13)

通过这种方式，一个包含33个节点的表达式树（ET）可以简洁地表示为两个总共只有15个节点的表达式树。通过这个简单的例子，我们希望展示所提出的染色体表示在有效压缩复杂表达式方面的优势。

此外，从上述示例可以看出，SL-GEP与GEP-ADF [23]的一个显著区别在于，我们的方法引入了C-ADFs，其输入参数可以是变量（例如x和z）、常量（例如π）、ADFs或主程序的任何子树。例如，在图6(a)中，主程序的根节点是一个带有两个输入参数的ADF。第一个输入参数是主程序的一个子树[即sin(G(x,z))]，而第二个输入参数是一个ADF[即G(x,π)]。

这一特性显著提高了染色体简洁表示复杂高阶表达式的能力。具体来说，表达式x^100可以表示为G*G*G*G*G*G*G*G*G*G，其中G=x^10，*在GEP-ADF中分别定义为ADF和链接函数。相比之下，在我们的SL-GEP中，通过简单地定义一个G(a)=a^10的C-ADF，相同的表达式可以更简洁地表示为G(G(x))。这不仅更简洁，而且更具可读性。

B. 提出的算法
SL-GEP的染色体表示是固定长度的，结构上与传统的基因表达相似。因此，GEP的搜索机制可以很容易地集成，以进化具有所提出表示的染色体。然而，GEP包含许多操作和控制参数，需要仔细调整。为了解决这个问题并进一步提高性能，本节提出了一种基于DE操作的新型搜索机制。
###基因表达编程 ###自动定义函数 ###染色体表示 ###表达式树 ###数据压缩
&&&&
SL-GEP的表示是固定长度的，并且在结构上与传统的基因表达（GEP）相似。因此，GEP的搜索机制可以很容易地集成到所提出的表示中，以进化染色体。然而，GEP包含许多操作和控制参数，需要仔细调整。为了解决这个问题并进一步提高性能，本节提出了一种基于差分进化（DE）操作的新型搜索机制。所提出的SL-GEP过程如算法1所示，它由四个主要步骤组成，即初始化、变异、交叉和选择。基本符号列于表II中。

1) 步骤1—初始化：第一步是生成NP个随机染色体以形成初始种群。如第III-A节所定义，每个染色体可以表示为符号向量，此处标记为目标向量：
X_i = [x_i,1, x_i,2, ..., x_i,D] (14)
其中i是种群中染色体的索引，D是染色体的长度，x_i,j是X_i的第j个元素。D的值通过以下公式计算：
D = h + l + K * (h' + l') (15)
其中K是每个染色体中ADF的数量。请注意，在本文中，所有函数和ADF的最大输入参数数量为两个，因此我们有l=h+1，l'=h'+1。x_i,j的值通过“随机分配”方案分配，该方案包含两个阶段。第一阶段是随机配置类型为函数、ADF、终端或输入参数。然而，分配的类型必须是可行的。例如，如果x_i,j属于主程序的尾部，那么x_i,j只能是终端类型。将分配类型的所有可行值集合表示为E，第二阶段涉及从E中随机选择一个可行值作为x_i,j的值。

算法1：SL-GEP
1 开始：
2 对于i=1到NP执行：
3 对于j=1到D执行：
4 x_i,j ← “随机分配”
5 评估初始种群
6 当终止条件未满足时执行：
7 更新函数和变量的频率
8 对于i=1到NP执行：
/*变异和交叉*/
9 F=rand(0,1)；CR=rand(0,1)
10 从当前种群中随机选择两个个体X_r1 ≠ X_i，和X_r2 ≠ X_i ≠ X_r1
11 设置k为1到D之间的随机整数
12 对于j=1到D执行：
13 计算变异概率φ（通过公式28）
14 如果(rand(0,1) < CR 或 j=k) 并且 (rand(0,1) < φ) 则：
15 u_i,j ← “基于频率的分配”
16 否则：
17 u_i,j = x_i,j
/*选择*/
18 如果f(U_i) < f(X_i) 则：
19 X_i = U_i;
20 结束

需要注意的是，初始化步骤随机初始化染色体，包括ADF。然后，染色体通过变异、交叉和选择等进化操作迭代进化。因此，ADF将随着SL-GEP搜索进行自学习，无需先验知识或手动配置。

2) 步骤2—变异：在第二步中，对每个目标向量执行变异操作以生成一个变异体。
###SL-GEP ###基因表达编程 ###差分进化 ###染色体进化 ###变异
&&&&
可行值来自xi,j的值。

需要注意的是，初始化步骤会随机初始化染色体，包括ADF。然后，染色体通过变异、交叉和选择等进化操作迭代演化。因此，ADF将与SL-GEP搜索一起自学习，无需先验知识或手动配置。

2) 步骤2——变异：在第二步中，对每个目标向量执行变异操作以生成一个变异向量。传统的DE变异表示为：
Yi = Xr1 + F · (Xr2 − Xr3) (16)
其中F是缩放因子，r1, r2, r3和i是四个不同的个体索引。

然而，由于染色体中的元素是离散符号，传统的DE数值操作不能直接使用。为了解决这个问题，我们将DE变异分解为三个阶段。第一阶段是获取当前种群中两个随机目标向量的差值（Δ1）（称为距离测量）：
Δ1 = (Xr2 − Xr3). (17)
第二阶段是通过系数F缩放差值（称为距离缩放）：
Δ1' = F · Δ1. (18)

第三阶段是将缩放后的差值添加到另一个随机目标向量以创建变异向量（称为距离添加）：
Yi = Xr1 + Δ1'. (19)

在树结构计算机程序的搜索空间中，上述三个阶段的实现如下。

a) 距离测量：在离散域中，两个元素之间的距离可以为零（即两个元素相同）或非零。这里我们使用“不关心”符号“*”来表示非零距离：
xi,j − xk,j = { 0, 如果xi,j与xk,j相同
              *, 否则 (20)
其中xi,j和xk,j分别是Xi和Xk的第j个元素值。例如，sin − exp = *；sin − sin = 0。通过这种方式，我们可以使用二进制差值向量获得(17)中的Δ1。然后使用(20)计算差值向量的每个维度。

b) 距离添加：为了便于理解，我们先描述第三阶段，再描述第二阶段。第三阶段将差值向量添加到目标向量，从而创建变异向量。显然，如果一个元素被添加到零距离，它将保持不变：
xi,j + 0 = xi,j. (21)
如果xi,j被添加到非零距离，它将演变为一个新值：
xi,j + * = a, a ∈ Ω1j (22)
其中Ω1j是Xi的第j个维度的可行值集合。新值a是根据“基于频率的分配”方案选择的，如算法2所述。在基于频率的分配方案中，如果xi,j ∈ ADF，它将以与随机分配方案相同的方式进行分配。否则，类型将根据种群中出现的可能类型的频率进行选择。特别是，在种群中出现频率更高的可行类型。
###基因表达式编程 ###差分进化 ###变异 ###离散域 ###染色体
&&&&
a, a ∈ Ω1j (22)
where Ω1j is the set of feasible values for the jth dimension of Xi. The new value 'a' is selected with a “frequency-based assignment” scheme, as described in Algorithm 2. In the frequency-based assignment scheme, if xi,j ∈ ADF, it will be assigned in the same way as in the random assignment scheme. Otherwise, the type is chosen based on the frequencies of the feasible types that appear in the population. Particularly, feasible types that appear more often in the population are more likely to be selected when using the frequency-based assignment scheme. The selection probability of 'a' is:
pa = (ca + c0) / Σb∈Ω1j (cb + c0) (23)
where ca is the frequency of 'a' in the main programs of all chromosomes in the population, and c0 is a small constant (e.g., c0 = 1). We introduce c0 to ensure that each feasible value has at least a small selection probability even though its frequency is near to zero or equals zero.

c) Distance scaling: In the second phase, the difference vector is scaled by a coefficient factor F. To achieve this, we make xi,j evolve into a new value at a mutation probability of φ, if it is added to a nonzero distance. The mutation probability is determined by:
φ = Σa∈Ω1j [F · (ca + c0) / Σb∈Ω1j (cb + c0)] = F. (24)

**Algorithm 2: Frequency-Based Assignment**
Input: The element to be mutated (I).
Output: The mutated element (I).
1 Begin:
2 if I ∈ H1 then
3 if rand(0,1) < θ then
4 I = Roulette-wheel(function set ∪ ADF set).
5 else
6 I = Roulette-wheel(terminal set)
7 else if I ∈ T1 then
8 I = Roulette-wheel(terminal set)
9 else if I ∈ H2 then
10 type = Rand({function, input argument})
11 if type = function then
12 I = Rand(function set)
13 else
14 I = Rand(input argument set)
15 else if I ∈ T2 then
16 I = Rand(input argument set)
17 End

In this way, a small F translates to a small mutation probability, which has the effect of making the mutant vector more similar to the base target vector.

To summarize, the above three phases enable the DE mutation to generate mutant vectors in a discrete space. In the SL-GEP, we use the commonly used “DE/current-to-best/1” mutation scheme as expressed by:
Yi = Xi + F · (Xbest - Xi) + F · (Xr1 - Xr2) (25)
where Xbest is the best individual in the population. The above mechanism can be easily extended to implement the DE/current-to-best/1. The computation process of (25) can be decomposed into two substeps, i.e., Ti = Xi + F · (Xbest - Xi) and Yi = Ti + F · (Xr1 - Xr2), where Ti = [ti,1, ti,2,..., ti,n] is a temporary vector. The probabilities of xi,j and ti,j remaining unchanged in the first and second substep are 1 - F · ψ(xpbest,j, xi,j) and 1 - F · ψ(xr1,j, xr2,j), respectively, where ψ(a,b) is defined as:
ψ(a,b) = {1, if a ≠ b; 0, otherwise.} (26)
Therefore, the probability of xi,j remaining unchanged after performing the two substeps is:
(1 - F · ψ(xbest,j, xi,j)) * (1 - F · ψ(xr1,j, xr2,j)). (27)
###频率赋值 ###距离缩放 ###变异概率 ###差分进化 ###SL-GEP ###--- ###**说明：** ###1. ###**删除无用字符 ###格式错误 ###重复内容：** ###* ###移除了公式中的乱码字符 ###如 ###`/Omega1j` ###替换为 ###`Ω1j` ###`/summationtext` ###替换为 ###`Σ` ###`/parenleftBigg` ###替换为 ###`[` ###或 ###`(` ###`/braceleftBigg` ###替换为 ###`{` ###等。 ###* ###修正了文本中的空格和标点符号 ###使其更符合英文书写规范。 ###* ###将 ###`I ###nt ###h ###e` ###修正为 ###`In ###the`。 ###* ###将 ###`coefﬁcient` ###修正为 ###`coefficient`。 ###* ###将 ###`proba-bility` ###修正为 ###`probability`。 ###* ###将 ###`muta-tion` ###修正为 ###`mutation`。 ###* ###将 ###`remain-ing` ###修正为 ###`remaining`。 ###* ###将 ###`deﬁned` ###修正为 ###`defined`。 ###* ###将 ###`a/negationslash=b` ###修正为 ###`a ###≠ ###b`。 ###* ###将 ###`function ###set/uniontextADF ###set` ###修正为 ###`function ###set ###∪ ###ADF ###set`。 ###* ###修正了公式 ###(23) ###和 ###(24) ###的排版 ###使其更清晰。 ###* ###修正了 ###Algorithm ###2 ###的格式 ###使其更易读。 ###* ###修正了公式 ###(27) ###的排版。 ###2. ###**修正明显的错别字和语法错误：** ###* ###`I ###nt ###h ###e` ###-> ###`In ###the` ###* ###`coefﬁcient` ###-> ###`coefficient` ###* ###`proba-bility` ###-> ###`probability` ###* ###`muta-tion` ###-> ###`mutation` ###* ###`remain-ing` ###-> ###`remaining` ###* ###`deﬁned` ###-> ###`defined` ###* ###`a/negationslash=b` ###-> ###`a ###≠ ###b` ###* ###确保了英文语法和拼写正确。 ###3. ###**保持原文的核心意思和逻辑结构：** ###* ###文本内容未进行实质性修改 ###仅对格式和字符进行了清洗 ###确保了原文关于频率赋值 ###距离缩放 ###变异机制以及DE/current-to-best/1变异方案的描述完整保留。 ###* ###Algorithm ###2 ###的步骤和逻辑完全保留。 ###* ###所有公式及其解释都保持不变。 ###4. ###**提取3-5个关键词：** ###* ###**频率赋值 ###(Frequency-Based ###Assignment):** ###文本中详细描述了一种基于频率的赋值方案 ###是核心概念之一。 ###* ###**距离缩放 ###(Distance ###Scaling):** ###文本中明确提到了距离缩放是第二阶段的关键操作。 ###* ###**变异概率 ###(Mutation ###Probability):** ###变异概率的计算和影响是文本的重要内容。 ###* ###**差分进化 ###(Differential ###Evolution ###DE):** ###文本讨论了DE变异在离散空间中的应用 ###并提到了DE/current-to-best/1方案。 ###* ###**SL-GEP:** ###文本中明确提到了SL-GEP是应用DE变异的上下文。
&&&&
临时向量。在第一和第二子步骤中，xi,j和ti,j保持不变的概率分别为 1 −F·ψ(xpbest,j,xi,j) 和 1 −F·ψ(xr1,j,xr2,j)，其中 ψ(a,b) 定义为：
ψ(a,b) = { 1, 如果 a ≠ b; 0, 否则。 (26)
因此，执行这两个子步骤后，xi,j保持不变的概率为：
(1−F·ψ(xbest,j,xi,j)) * (1−F·ψ(xr1,j,xr2,j))。(27)
因此，xi,j的变异概率为：
ϕ = 1−(1−F·ψ(xbest,j,xi,j)) * (1−F·ψ(xr1,j,xr2,j))。(28)
为了提高算法的鲁棒性并减少控制参数的数量，我们还采用随机方案来设置 DE/current-to-best/1 变异方案中的 F 值：
F = rand(0,1) (29)
其中 rand(a,b) 返回在 [a,b] 范围内均匀分布的随机值。

3) 步骤3—交叉：在第三步中，每个目标向量 Xi 与其变异向量 Yi 进行交叉，以创建试探向量 Ui：
ui,j = { yi,j, 如果 rand(0,1) < CR 或 j=k; xi,j, 否则。(30)
其中 CR 是交叉率，k 是 1 到 D 之间的随机整数，ui,j、yi,j 和 xi,j 分别是 Ui、Yi 和 Xi 的第 j 个变量。与 F 类似，CR 的值设置为：
CR = rand(0,1)。

4) 步骤4—选择：最后，在第四步中，选择目标向量和试探向量每对中较优的解决方案，以形成新的种群：
Xi = { Ui, 如果 f(Ui) < f(Xi); Xi, 否则。(31)
其中 f(X) 返回 X 的适应度值。

第二步和第四步之间存在重复，直到满足终止条件。

总而言之，上述四个步骤扩展了 DE 搜索机制，以演化编码的解决方案。值得注意的是，所提出的 SL-GEP 是一个通用框架，因此其他最先进的 DE，如 JADE [31]、CoDE [32] 和其他 [33]、[34] 可以很容易地用作替代方案。接下来，我们将从计算复杂度和控制参数大小方面研究所提出的算法与 GEP 和 GEP-ADF。根据上述过程，所提出的 SL-GEP 在每一代中的计算复杂度是两部分的总和：1) 生成 NP 个新染色体；2) 将 NP 个新染色体解码为 ET 并评估它们的适应度值。函数和变量的频率可以通过一次扫描种群中的元素来更新，其复杂度为 O(NP·D)。基于频率的分配方案选择一个元素是轮盘赌选择过程。通过使用 [35] 中提出的方法，上述基于频率的分配操作的复杂度可以降低到 O(1)。因此，变异和交叉的复杂度为 O(NP·D)，第一部分的复杂度为 O(NP·D)。第二部分的复杂度...
###SL-GEP ###变异概率 ###交叉 ###选择 ###计算复杂度
&&&&
变量可以通过单次扫描群体中的元素来更新，其复杂度为O(NP·D)。基于频率的分配方案选择一个元素是轮盘赌选择过程。通过使用[35]中提出的方法，上述基于频率的分配操作的复杂度可以降低到O(1)。因此，变异和交叉的复杂度为O(NP·D)，第一部分的复杂度为O(NP·D)。第二部分的复杂度是问题特定的，但对于所有GEP变体都是相同的。将第二部分的复杂度表示为O(f)，则所提出的SL-GEP在每一代中的复杂度为O(NP·D)+O(f)。因此，我们可以得到GEP和GEP-ADF的复杂度为O(NP·D)+O(f)。由此可见，我们提出的SL-GEP算法、GEP和GEP-ADF的复杂度是相似的。同时，如表III所示，所提出的SL-GEP算法只有四个控制参数，而标准GEP和GEP-ADF分别包含十一个和二十个控制参数。从这个角度来看，所提出的SL-GEP算法包含的控制参数更少，因此更方便和适用于实际使用。

**表III：GEP、GEP-ADF和SL-GEP中的控制参数数量**

**C. 常量创建**
数值常量是大多数数学公式不可或缺的一部分。因此，数值常量的创建是GP及其变体演化出令人满意的数学公式的重要组成部分。然而，对于GP类方法来说，精确逼近常数值是相当具有挑战性的，因为数值常量是连续值，而GP类方法的染色体表示通常适用于组合优化。在文献中，已经提出了几种解决常量创建问题的方法。最常见的一种是Koza [1]引入的“瞬时随机常量（ERC）”。在Koza的方法中，ERC被视为一个特殊的终结符。在创建初始群体时，每个ERC的值在特定范围内随机分配。然后，随机ERC是固定的，并通过交叉操作从一个解析树移动到另一个解析树。Ferreira [36]提出了一种处理GEP中常量的新方法。在Ferreira的方法中，一个额外的终结符“?”用于表示公式中的常量。在初始化时，随机创建一个常量池并分配给每个个体。在解码基因表达染色体以进行适应度评估时，每个“?”都相应地分配常量池中的一个常量。引入了一个额外的dc域和一些特殊的dc操作来促进常量创建过程。除了上述两种方法外，其他方法如局部搜索方法[37]、非线性最小二乘最小化[38]和进化算法[39]也已被用于搜索常数值。
###复杂度 ###控制参数 ###常量创建 ###SL-GEP ###GEP
&&&&
在初始化过程中，每个个体都会被创建并分配。当解码基因表达染色体进行适应度评估时，每个“？”都会根据常量池中的常量进行分配。为了方便常量创建过程，引入了一个额外的dc域和一些特殊的dc操作。除了上述两种方法，其他方法如局部搜索法[37]、非线性最小二乘最小化[38]和进化算法[39]也曾被用于搜索常量值。

与GEP[8]一样，常量创建操作在所提出的SL-GEP中被视为可选操作。当在搜索过程中考虑常量时，SL-GEP由于其简单性而采用常用的ERC来处理常量。值得注意的是，其他现有的常量处理方法也可以轻松地应用于所提出的SL-GEP中。具体来说，在初始化步骤中，已经生成了一组特定范围（例如，[-1, 1]）内的固定随机常量。引入了一个新的终端符号来表示ERC。在随机分配和基于频率的分配过程中，H1和T1的每个元素都有可能被分配一个常量。当一个元素需要被分配一个常量时，将从常量集中选择一个随机常量。分配给该元素的常量将保持固定，除非对其执行基于频率的分配突变。

**IV. 实验与比较**
本节研究了所提出的SL-GEP的性能。首先，介绍了实验设置，包括基准测试问题和用于比较的性能指标。然后，将所提出的SL-GEP与GEP、GEP-ADF、GP和两种最近发布的GP变体进行了评估。最后，研究了SL-GEP重要控制参数的影响。

**A. 实验设置**
本节通过解决两类已建立的问题来评估SL-GEP的性能。第一类包含15个符号回归问题，如表IV所示。这些基准问题选自[26]和[40]。其中，F1-F14是常用的基准问题，它们在目标公式方面具有独特的结构复杂性。F15源于一个工业问题，涉及对蒸馏塔组成的气相色谱测量进行建模。该问题包含4999条记录，每条记录包含25个潜在输入变量和一个输出值。

在表IV中，最后一列描述了要拟合的数据集，其中U[a,b,c]表示从a到b的c个均匀随机样本。如[26]所建议，所有15个问题的功能集都设置为{+,-,×,÷,sin,cos,ex,ln(|x|)}。

第二类是k偶校验问题。
###SL-GEP ###常量处理 ###符号回归 ###基因表达编程 ###实验评估
&&&&
本文讨论了蒸馏塔组成的气相色谱测量建模问题。该问题包含4999条记录，每条记录包含25个潜在输入变量和一个输出值。在表IV中，最后一列描述了待拟合的数据集，其中U[a,b,c]表示从a到b的c个均匀随机样本。根据[26]的建议，所有15个问题的函数集设置为{+,-,×,÷,sin,cos,ex,ln(|x|)}。F15数据集可从http://symbolicregression.com/sites/default/files/DataSets/towerData.txt下载。

第二类问题是k偶校验问题，需要找到一个包含k个参数的合适布尔公式。当且仅当有偶数个参数被赋值为真时，该布尔公式应返回真值。偶校验问题是评估遗传编程（GP）的流行基准问题[26]。对于盲随机搜索和传统GP而言，这些布尔优化问题非常困难。本文在第二类问题中考虑了六个偶校验问题，即三校验到八校验问题。根据[22]的建议，这六个偶校验问题的函数集设置为{AND,OR,NAND,NOR}。

选择了七种GP变体与所提出的SL-GEP进行比较。第一种算法是传统的GEP[5]。第二种算法是GEP-ADF[23]，它是GEP与ADF结合的初步版本。第三种是基于ECJ库开发的GP系统[41]。第四种是LDEP[42]，它将差分进化（DE）与线性GP相结合。第五种是基于树的DE（TreeDE）[43]，它是用于解决符号回归问题的DE的离散版本。第六种是名为GEP-ADF2的修改版SL-GEP，它用GEP的传统操作（例如，选择、变异、单点交叉和两点交叉）取代了所提出的基于DE的搜索机制。我们将SL-GEP与GEP-ADF2进行比较，以分析所提出的基于DE的搜索机制的有效性。最后一种是SL-GEP的增强版本（标记为SL-GEP/JADE），它用JADE[31]中的DE/current-to-pbest/1策略取代了SL-GEP中经典的DE/current-to-best/1变异策略。SL-GEP/JADE还采用了JADE的自适应参数控制策略，以自适应地调整F和CR。引入SL-GEP/JADE只是为了证明所提出的SL-GEP提供了一个通用框架，可以轻松容纳不同的搜索机制。

表V列出了所考虑算法的参数设置。TreeDE和LDEP的参数根据其原始论文中的建议进行配置。根据[44]的建议，GP的NP设置为1024，其他参数与ECJ库中的默认设置相同。GEP和GEP-ADF的参数根据Ferreira在[23]中的建议设置。
###遗传编程 ###偶校验问题 ###符号回归 ###差分进化 ###算法比较
&&&&
表V列出了所考虑算法的参数设置。TreeDE和LDEP的参数根据其原始论文中的建议进行配置。正如[44]所建议的，GP的NP设置为1024，其他参数与ECJ库中的默认设置相同。GEP和GEP-ADF的参数设置参考了Ferreira在[23]中的建议。在GEP和GEP-ADF的原始论文中，作者没有给出固定的头部长度设置规则，而是建议根据不同类型的问题使用不同的头部长度。通常，问题中的变量数量越多，应使用越长的头部长度。在我们的实验研究中，头部长度是根据问题的变量大小凭经验设置的。为了公平比较，我们对所有GEP变体的头部长度进行了固定：对于F1-F14等小变量规模问题，设置为10；对于F15和六个偶校验问题等大变量规模问题，设置为20。

对于LDEP，建议的寄存器数量为6，这对于解决变量数量大于6的大规模偶校验问题和F15是不可行的。为了解决这个问题，LDEP的寄存器数量在六个偶校验问题中设置为12，在F15中设置为40。我们的实验研究表明，这些设置产生了有希望的结果。

对于需要常数的问题（即F13、F14和F15），GP使用了ECJ库中实现的Koza的ERC，而GEP、GEP-ADF和GEP-ADF2使用了[8]中描述的Ferreira方法。LDEP使用了其原始论文中提出的特殊常数创建机制，而我们提出的SL-GEP和SL-GEP/JADE则考虑了第三-C节中描述的方法。对于所有问题，当评估次数达到最大值1,000,000（即Emax=1,000,000）时，每个算法将终止。

B. 性能评估指标

对于15个符号回归问题，采用十折交叉验证方法进行训练和测试。具体来说，对于每个问题，数据集被平均分为十份。对于每次EA运行，九份用于训练，剩余的一份用于测试找到的最佳解决方案。共有十种不同的情况，我们对每种情况下的每个算法重复运行十次，使用不同的随机种子。因此，每个算法在每个问题上总共有100次不同的运行。在训练阶段，使用九份数据评估每个解决方案的适应度，如（2）所示。当算法收敛到解决方案Si，且f(Si)<10^-4时，则认为搜索成功收敛或完美命中。在每次EA运行结束时，使用（2）基于剩余的数据对获得的最佳解决方案进行测试。100次EA运行的平均测试结果用于比较分析。至于六个偶校验问题，
###算法参数 ###头部长度 ###寄存器数量 ###交叉验证 ###性能评估 ###**说明：** ###1. ###**删除无用字符 ###格式错误 ###重复内容：** ###删除了开头的"nt ###search ###mechanisms ###can ###be ###easily ###accommodated." ###以及一些不必要的换行和标点符号 ###使文本更流畅。 ###2. ###**修正明显的错别字和语法错误：** ###* ###"Table ###Vlists" ###改为 ###"表V列出了" ###* ###"con-ﬁgured" ###改为 ###"配置" ###* ###"NPof ###GP" ###改为 ###"GP的NP" ###* ###"Ferreira ###in ###[ ###23]" ###改为 ###"Ferreira在[23]中" ###* ###"ﬁxed ###rule" ###改为 ###"固定的规则" ###* ###"rule ###ofthumb" ###改为 ###"通常" ###* ###"larger ###number ###of ###variables ###a ###problem ###has ###a ###larger ###head ###length ###should ###be ###used." ###调整为更自然的中文表达。 ###* ###"ﬁxed ###the ###head ###lengths ###of ###all ###GEP ###variants ###to ###be ###10 ###for ###solving ###small ###variable ###size ###problems ###such ###as ###F1−F14 ###while ###20 ###for ###solving ###large ###size ###problems ###like ###F15and ###the ###six ###even-parity ###problems." ###调整为更清晰的中文表达。 ###* ###"infeasible ###for ###solving ###large-scale ###even-parity ###problems ###and ###F15 ###where ###the ###numbers ###of ###variables ###are ###larger ###than ###6." ###调整为更自然的中文表达。 ###* ###"produced ###promising ###results." ###改为 ###"产生了有希望的结果。" ###* ###"Koza’s ###ERC ###that ###was ###implemented ###in ###the ###ECJ ###library" ###改为 ###"ECJ库中实现的Koza的ERC" ###* ###"Section ###III-C" ###改为 ###"第三-C节" ###* ###"1 ###000 ###000" ###改为 ###"1 ###000 ###000" ###* ###"Speciﬁcally" ###改为 ###"具体来说" ###* ###"tenfold" ###改为 ###"十份" ###* ###"ninefold" ###改为 ###"九份" ###* ###"f(Si)<10−4" ###改为 ###"f(Si)<10^-4" ###* ###删除了末尾不完整的句子 ###"As ###for ###the ###six ###even-parity ###problems ###"。 ###3. ###**保持原文的核心意思和逻辑结构：** ###整体上保留了原文关于算法参数设置 ###头部长度和寄存器数量的调整 ###常数处理方法以及性能评估指标和交叉验证方法的描述。 ###4. ###**提取3-5个关键词：** ###选择了“算法参数” ###“头部长度” ###“寄存器数量” ###“交叉验证” ###“性能评估”这五个核心概念作为关键词。
&&&&
对于每个问题，每个算法都进行独立运行。在训练阶段，使用九折数据评估每个解决方案的适应度，如公式（2）所示。当算法收敛到适应度f(Si)<10−4的解决方案Si时，认为搜索成功收敛或完美命中。在每次EA运行结束时，使用剩余折数据，根据公式（2）测试获得的最佳解决方案。100次EA运行的平均测试结果用于比较分析。对于六个偶校验问题，训练数据是所有可能的输入分配和相应的输出。例如，三校验问题包含2^3=8个不同的输入和输出对。这八个输入和输出对用作训练数据。每个解决方案的适应度值根据公式（2）使用所有训练数据进行评估。由于偶校验问题没有测试数据，因此对于每个算法，我们对每个问题进行了100次独立运行。然后报告100次运行的平均训练性能。

在实证研究中，第一个考虑的性能指标是公式（2）给出的测试准确性。该指标被认为是评估算法性能最重要的指标。此外，如文献[45]所建议，实现完美命中的成功率（表示为Suc）被采纳为第二个指标。Suc通过以下公式计算：
Suc = Cs / C * 100% (32)
其中C是独立运行的次数，Cs是实现完美命中的成功运行次数。

此外，实现完美命中所需的适应度评估次数（表示为运行时间，RT）被采纳为第三个性能指标。该指标表明了算法的收敛速度。如果算法未能实现完美命中，则考虑文献[46]中描述的方法来估计RT：
RT = Es + 1 - Suc / Suc * Emax (33)
其中Es是成功运行实现完美命中的平均适应度评估次数，Emax是最大适应度评估次数。

C. 与GEP和GEP-ADF2的比较
表VI总结了GEP、GEP-ADF2和SL-GEP获得的Suc和RMSE。RMSE是基于十折交叉验证的100次独立运行的平均测试准确性。对于每个问题，进行Wilcoxon符号秩检验，以检测两种算法之间的显著差异。首先，我们评估GEP-ADF2与传统GEP[5]的比较。从表VI可以看出，GEP-ADF2在21个问题中的11个问题上根据RMSE显著优于GEP，并在其余十个问题上表现出竞争力。特别是，GEP-ADF2在所有六个偶校验问题上报告了更高的Suc，而GEP未能找到最后一个问题的全局最优解。
###算法性能 ###适应度评估 ###成功率 ###收敛速度 ###GEP-ADF2 ###**说明：** ###1. ###**删除无用字符 ###格式错误 ###重复内容：** ###移除了“nt ###runs ###for” ###“TABLE ###VI” ###“TABLE ###VII” ###“74 ###IEEE ###TRANSACTIONS ###ON ###EVOLUTIONARY ###COMPUTATION ###VOL. ###20 ###NO. ###1 ###FEBRUARY ###2016”等无关或格式错误的内容。 ###2. ###**修正明显的错别字和语法错误：** ###* ###“ninefold ###of ###data”修正为“九折数据”。 ###* ###“ﬁtness”修正为“适应度”。 ###* ###“perfect ###hit ###is ###assumed”修正为“认为搜索成功收敛或完美命中”。 ###* ###“even-parity ###problems”统一翻译为“偶校验问题”。 ###* ###“three-parity ###problem”修正为“三校验问题”。 ###* ###调整了部分句子的语序 ###使其更符合中文表达习惯 ###例如将“nt ###runs ###for ###each ###algorithm ###on ###each ###problem”调整为“对于每个问题 ###每个算法都进行独立运行”。 ###* ###修正了公式中的变量名称 ###使其与上下文一致。 ###* ###修正了“Suc=Cs ###C·100% ###(32)”为“Suc ###= ###Cs ###/ ###C ###* ###100% ###(32)” ###并解释了变量。 ###* ###修正了“RT=E ###s+1−Suc ###SucEmax ###(33)”为“RT ###= ###Es ###+ ###1 ###- ###Suc ###/ ###Suc ###* ###Emax ###(33)” ###并解释了变量。 ###* ###修正了“TABLE ###VIsummaries”为“表VI总结了”。 ###* ###修正了“GEP-ADF2 ###signiﬁcantly ###outperformed ###GEP ###on ###11 ###out ###of ###the ###21 ###problems”为“GEP-ADF2在21个问题中的11个问题上根据RMSE显著优于GEP”。 ###3. ###**保持原文的核心意思和逻辑结构：** ###文本的整体结构和各段落的主题保持不变 ###包括实验设置 ###性能指标定义 ###以及GEP-ADF2与GEP的比较结果。 ###4. ###**提取3-5个关键词：** ###选择了“算法性能” ###“适应度评估” ###“成功率” ###“收敛速度” ###“GEP-ADF2”作为关键词 ###它们能概括文本的主要内容。
&&&&
从表VI可以看出，GEP-ADF2在21个问题中的11个问题上，根据RMSE显著优于GEP，并在其余10个问题上表现出竞争力。特别是，GEP-ADF2在所有六个偶校验问题上都报告了更高的成功率，而GEP未能找到最后四个问题的全局最优解。这是因为大规模偶校验问题的解表达式变得极其复杂。因此，对于传统的GEP来说，这些问题非常难以解决，尤其是在不使用子函数的情况下。

除了偶校验问题，GEP-ADF2在F2-F6问题上也表现出更好的性能。进一步的分析和验证表明，这些问题的解决方案可以通过使用ADF（自动定义函数）有效地压缩。例如，F5的原始表达式是“x\*x\*x\*x\*x+x\*x\*x\*x+x\*x\*x+x\*x+x”，包含29个符号。通过使用“G(a,b)=b+b\*a”作为ADF，F5可以被压缩为“G(G((x\*x),G(x,x)),x)”，包含的符号数量大大减少。表VII展示了GEP-ADF2在F1-F6问题和六个偶校验问题上找到的其他几个解决方案。值得注意的是，收敛的解决方案非常简洁，这得益于ADF的使用。GEP-ADF2需要额外的计算资源来搜索有前景的ADF。因此，在F4和F1等简单问题上，使用ADF的益处并不显著。然而，随着问题复杂性的增加，ADF的益处变得更加明显和显著，这可以从F5、F6以及六个偶校验问题的结果中观察到。至于F7-F12，它们的原始表达式只包含少量符号。因此，它们可以在不使用ADF的情况下简洁地表达。因此，GEP-ADF2在这些问题上的性能与GEP相似。这些结果表明，所提出的GEP-ADF2可以有效地利用ADF来提高GEP的搜索精度。

接下来，我们评估SL-GEP与GEP-ADF2，以研究所提出的基于DE（差分进化）的离散问题搜索机制的有效性。可以观察到，SL-GEP在12个问题上显著优于GEP-ADF2，并在其余9个问题上表现出竞争力（根据RMSE）。然而，根据成功率值，SL-GEP在12个问题上获得了100%的成功率，这优于GEP-ADF2。此外，SL-GEP在其余9个问题上的成功率值被观察到远优于或至少与GEP-ADF2相当。这些结果表明，所提出的基于DE的搜索机制有助于进一步提高GEP-ADF2的性能。
###GEP-ADF2 ###ADF ###偶校验问题 ###性能提升 ###SL-GEP
&&&&
GEP-ADF2在12个问题上表现出竞争力，在其余9个问题上，就RMSE而言，其表现也具有竞争力。然而，根据成功率（Suc）值，SL-GEP在12个问题上获得了100%的成功率，这优于GEP-ADF2。此外，SL-GEP在其余9个问题上的成功率值被观察到远优于或至少与GEP-ADF2相当。这些结果表明，所提出的基于DE的搜索机制有助于进一步提高GEP-ADF2的性能。

此外，我们还进行了多问题Wilcoxon检验，以检查GEP、GEP-ADF2和SL-GEP在测试套件上的行为。表VIII总结了统计结果。多问题Wilcoxon检验的结果再次表明，GEP-ADF2表现出比GEP显著更好的性能，而所提出的SL-GEP表现出比GEP和GEP-ADF2都显著更好的性能，概率误差p<0.05。

**D. 与其他GP变体的比较**

本节评估了SL-GEP与GP、GEP-ADF、TreeDE、LDEP和SL-GEP/JADE算法的结果。表IX报告了所比较算法的成功率和RMSE。为了评估多种算法在多个问题上的性能，我们首先应用了Friedman检验来检测所有算法获得的平均RMSE值之间是否存在显著差异，如[47]中所述。表X给出了α=0.05时Friedman检验的结果。统计Friedman值为59.9451，大于临界值11.07。这表明算法获得的结果之间存在显著差异，概率误差p<0.05。接下来，我们还采用了Bonferroni-Dunn检验作为事后检验，以检测控制算法SL-GEP的显著差异。Bonferroni-Dunn检验在α=0.05时的临界差（CD）值为1.484。图7绘制了通过Friedman检验获得的排名和Bonferroni-Dunn程序CD的阈值。阈值等于CD值加上SL-GEP的排名（即1.484 + 1.8333 = 3.3173）。排名大于阈值的算法被认为显著差于SL-GEP。

可以观察到，就RMSE而言，SL-GEP表现出比GP、GEP-ADF、TreeDE和LDEP显著更好的性能。同时，由于SL-GEP的排名小于SL-GEP/JADE的排名加上CD，因此SL-GEP和SL-GEP/JADE的性能被认为是具有竞争力的。表IX的最后三行总结了每个问题上Wilcoxon符号秩检验的结果。值得注意的是，所提出的SL-GEP表现出显著更好的性能。
###SL-GEP ###GEP-ADF2 ###RMSE ###Friedman检验 ###Wilcoxon检验
&&&&
本文对SL-GEP算法的性能进行了统计检验。在RMSE指标上，SL-GEP显著优于GP、GEP-ADF、TreeDE和LDEP。同时，SL-GEP和SL-GEP/JADE的性能具有竞争力。

Wilcoxon符号秩检验结果显示，SL-GEP在大多数问题上显著优于GP、GEP-ADF、TreeDE和LDEP，而SL-GEP和SL-GEP/JADE的性能相当。多问题Wilcoxon检验进一步证实，在RMSE指标上，SL-GEP显著优于GP、GEP-ADF、TreeDE和LDEP，而SL-GEP和SL-GEP/JADE在α=0.05水平上没有显著差异。

在成功率（Suc）方面，SL-GEP在大多数问题上优于GP、GEP-ADF、TreeDE和LDEP。特别是对于偶数奇偶校验问题，尽管GP、GEP-ADF、TreeDE和LDEP在三位奇偶校验问题上达到了100%的成功率，但随着问题维度的增加，它们的成功率显著下降。GEP-ADF、TreeDE和LDEP未能解决五位、六位、七位和八位奇偶校验问题。相比之下，SL-GEP在偶数奇偶校验问题上始终保持100%的成功率。综上所述，SL-GEP在成功率指标上优于GP、GEP-ADF、TreeDE和LDEP。

此外，本文还分析了算法的收敛速度。在运行时间（RT）方面，SL-GEP在大多数问题上优于除SL-GEP/JADE之外的所有算法。GEP-ADF2由于未使用基于DE的搜索机制，在所有18个问题上均不如SL-GEP，这表明所提出的基于DE的算子比原始基于遗传的算子更高效。同时，SL-GEP/JADE在大多数问题上RT优于SL-GEP，这表明SL-GEP可以与其他先进的差分进化算法结合，进一步提高搜索性能。
###SL-GEP ###统计检验 ###性能评估 ###收敛速度 ###差分进化
&&&&
GEP-ADF2 未使用所提出的基于DE的搜索机制，因此在所有18个问题上均不如SL-GEP。这表明所提出的基于DE的算子比原始基于遗传的算子效率更高。同时，SL-GEP/JADE在大多数问题上都优于SL-GEP。这表明所提出的SL-GEP可以与其他最先进的DE形式集成，以进一步提高搜索性能。

此外，我们将所提出的SL-GEP的RT结果与ECGP的已发表结果进行了比较。在[48]中，ECGP应用于五个偶校验问题，即四校验到八校验问题。ECGP（SL-GEP）在这五个问题上的RT值分别为65296（36001）、181920（64224）、287764（94542）、311940（158146）和540224（254855）。很明显，所提出的SL-GEP比ECGP具有更快的收敛速度，因为ECGP的RT值几乎是所提出的SL-GEP的两倍。

接下来，我们研究问题维度对算法性能的影响。图9显示了RT与偶校验问题维度的关系。ECGP的已发表结果也绘制出来进行比较分析。可以观察到，GP、GEP、GEP-ADF、TreeDE和LDEP的RT随着偶校验问题维度的增加而急剧增加，而我们提出的GEP-ADF2、SL-GEP和SL-GEP/JADE的增加速度要慢得多。随着偶校验问题维度的增加，所提出的算法显示出比ECGP更好的RT值。因此，结果表明所提出的算法比其他同类算法具有更高的可伸缩性。

图8描绘了算法在六个代表性问题上获得的最佳适应度值的搜索收敛趋势：1）F1；2）F5；3）F10；4）F15；5）三校验问题；6）八校验问题。在图中，请注意当达到全局最优时，搜索轨迹终止。可以观察到，所提出的SL-GEP比GEP、GEP-ADF、TreeDE和LDEP以更快的收敛速度收敛到全局最优或高质量解决方案。GP也显示出非常快的收敛速度（例如，F10），但它通常很快陷入局部最优。

本节展示了所提出的SL-GEP算法找到的一些收敛解。我们的目标是分析收敛解的简洁性和可读性。表VI报告了结构复杂性。图8显示了所有比较算法在(a) F1、(b) F5、(c) F10、(d) F15、(e) 三校验问题和(f) 八校验问题上获得的最佳适应度值的演变。图9显示了RT与偶校验问题维度的关系。（对于GP、GEP、GEP-ADF、TreeDE和LDEP，它们在大规模问题上的RT值是...）
###SL-GEP ###RT值 ###收敛速度 ###可伸缩性 ###偶校验问题
&&&&
本文旨在分析SL-GEP算法收敛解的简洁性和可读性。表VI报告了F5、F10、三奇偶问题和八奇偶问题上收敛解的结构复杂性。这些解都达到了完美的命中。如果算法在100次独立运行中未能找到完美命中的解，则相应值在表中标记为“N/A”。为了量化收敛解的复杂性，本文采用了[49]中提出的复杂性度量。该度量根据所有子树中的节点总数来确定表达式的结构复杂性。图10说明了确定ET复杂性的一个示例。该度量偏爱层数和节点较少的树，并被证明可有效定义表达式的结构复杂性[40]，[49]。在我们的实验研究中，解的结构复杂性等于主程序和ADF的结构复杂性之和。由于LDEP找到的解包含许多低级指令，因此其解在表XIII中省略。

图8展示了所有比较算法在(a) F1、(b) F5、(c) F10、(d) F15、(e) 三奇偶问题和(f) 八奇偶问题上最佳适应度值的演变。图9显示了RT与偶奇偶问题维度的关系。(对于GP、GEP、GEP-ADF、TreeDE和LDEP，它们在大规模问题上的RT值缺失，因为它们在Emax = 1,000,000的100次运行中未能找到全局最优解。ECGP的结果引用自[48])。图10是计算表达式结构复杂度的示例。

可以观察到，SL-GEP提供的解通常更具可读性，因为在大多数情况下它们的结构复杂性较低。具体而言，在第一个符号回归问题上，SL-GEP优于GP、GEP、GEP-ADF和TreeDE。至于第二个符号问题，GP、GEP和GEP-ADF略优于SL-GEP，因为该问题的表达式可以在不使用ADF的情况下简洁地表达。在三奇偶问题上，SL-GEP显著优于GP、GEP、GEP-ADF和TreeDE，因为其解的结构复杂性远小于其他四种算法。在比三奇偶问题复杂得多的八奇偶问题上，GP、GEP、GEP-ADF和TreeDE都未能在其搜索中找到全局最优解。然而，SL-GEP能够收敛到八奇偶问题上的全局最优解。此外，SL-GEP在八奇偶问题上提供的解具有相对较小的结构复杂性。

表XIII列出了GP、GEP、GEP-ADF、TreeDE和SL-GEP找到的最佳解示例。
###SL-GEP ###结构复杂性 ###可读性 ###奇偶问题 ###算法比较
&&&&
在奇偶校验问题中，GP、GEP、GEP-ADF和TreeDE都未能在搜索中找到全局最优解。然而，SL-GEP能够收敛到八位奇偶校验问题的全局最优解。此外，SL-GEP在八位奇偶校验问题上提供的解决方案具有相对较小的结构复杂性，这与GEP-ADF在三位奇偶校验问题上找到的解决方案相似。

G. 算法参数分析
SL-GEP涉及四个重要参数：NP、h、h/prime和K。本节通过在三个具有代表性的符号回归问题（F1、F6和F11）上使用不同的参数设置来研究它们的影响。F1和F6分别代表一种简单和一种复杂的符号回归问题，它们的解可以通过ADF有效压缩，而F11代表另一种符号回归问题，其解可以不使用ADF简洁地表达。

1) NP的影响：首先，我们研究NP的影响。我们将NP的值分别设置为20、50、100、400和1000，而其他参数与表V中保持一致。对于每种参数设置，进行了100次独立运行。表XIV显示的结果表明，NP不应设置得过小或过大。如果NP设置得过小，算法可能由于种群多样性丧失而容易陷入局部最优。例如，当NP减小到20时，SL-GEP在F6上的成功率下降。同时，较大的NP会减慢搜索速度。对于这三个测试实例，当NP从50增加到1000时，SL-GEP通常需要更大的计算成本。看来NP=50和NP=100是很有前景的设置。

2) h的影响：一般来说，较大的h使主程序能够表示更复杂的树结构，但这也会导致更大的搜索空间。为了评估h的影响，我们将h的值分别设置为3、5、10、20和40，而其他参数与表V中保持一致。表XV显示的结果表明，h不应设置得过小。如果h过小，搜索空间中将没有解决方案。例如，当h=3时，SL-GEP在100次运行中都未能找到F6的最优解。另一方面，随着h的增加，搜索空间会扩大。因此，SL-GEP通常需要更大的计算成本。表XV的结果表明，当h从20增加到40时，SL-GEP的性能逐渐下降。

3) h/prime的影响：h/prime决定了ADF的头部长度。通常，具有较大h/prime的ADF可以完成更复杂的子任务，但这也会导致更大的搜索空间。
###SL-GEP ###参数分析 ###奇偶校验问题 ###符号回归 ###算法优化
&&&&
在所有100次运行中，SL-GEP在F6上获得了最优解。另一方面，随着h的增加，搜索空间会增大。因此，SL-GEP通常需要更大的计算成本。表XV的结果表明，当h从20增加到40时，SL-GEP的性能逐渐下降。

3) h/prime的影响：h/prime决定了ADF的头部长度。通常，具有较大h/prime的ADF可以完成更复杂的子任务，但这也会导致更大的搜索空间。我们分别将h/prime设置为1、2、3、5和10，以研究其影响。表XVI的结果显示，当h/prime减小到1时，算法在F1和F6上的性能显著下降。然而，对于F11，h/prime的值似乎对算法的性能影响很小。这是因为F1和F6的表达式可以通过使用ADF有效压缩，而F11的表达式即使不使用ADF也已经足够简洁。如果h/prime=1，每个染色体中的ADF过于简单，无法有效提高搜索效率。同时，随着h/prime的增加，每个染色体中的ADF变得不那么通用（即，不太可能成为频繁的子结构）。因此，当h/prime变得过大时，算法在这两个问题上的性能下降。总的来说，h/prime=2和h/prime=3会带来更好的性能。

4) K的影响：参数K是每个染色体中ADF的数量。为了评估其影响，我们分别将其值设置为1、2、5、10和20。表XVII的结果显示，K对算法解决F11的性能影响很小，因为F11的解表达式无需使用ADF即可简洁表示。然而，当K过小（例如K=1）或过大（例如大于5）时，算法在F1和F6上的性能显著下降。K的值似乎应设置在2到5之间。

V. 结论
本文提出了一种用于自动生成计算机程序的SL-GEP方法。所提出的SL-GEP具有一种新颖的染色体表示，有助于形成C-ADF，该C-ADF包含ADF和/或主程序的任何子树作为输入参数。此特性使算法更灵活，能够获得复杂且具有建设性的C-ADF，从而提高搜索的准确性和效率。此外，提出了一种基于DE的新型搜索机制，以有效地进化SL-GEP中的染色体。在15个符号回归问题和6个偶校验问题上的实验表明，所提出的SL-GEP在准确性和搜索效率方面通常优于几种最先进的GP变体。此外，SL-GEP能够提供更具可读性的解决方案，这些解决方案具有更小的结构复杂性。未来有几个有趣的研究方向。
###SL-GEP ###h/prime ###K ###搜索空间 ###性能影响
&&&&
本文提出了一种新颖的基于差分进化的搜索机制，以高效地演化SL-GEP中的染色体。在15个符号回归问题和6个偶校验问题上的实验表明，所提出的SL-GEP在准确性和搜索效率方面通常优于几种最先进的遗传编程（GP）变体。此外，SL-GEP能够提供结构复杂度更小、更具可读性的解决方案。

未来有几个有趣的研究方向。一个方向是通过在进化过程中将结构复杂度作为另一个目标来扩展所提出的SL-GEP。通过结合多目标优化技术，扩展算法可以提供在准确性和可读性之间进行权衡的多种替代解决方案。第二个方向是通过自适应地控制SL-GEP的参数（例如染色体长度和每个染色体中ADF的数量）来进一步增强SL-GEP。另一个有前景的研究课题是将所提出的SL-GEP应用于复杂的实际应用。

**参考文献：**
[1] J. R. Koza, Genetic Programming: On the Programming of Computers by Means of Natural Selection, vol. 1. Cambridge, MA, USA: MIT Press, 1992.
[2] P. G. Espejo, S. Ventura, and F. Herrera, “A survey on the application of genetic programming to classification,” IEEE Trans. Syst., Man, Cybern., Appl. Rev., vol. 40, no. 2, pp. 121–144, Mar. 2010.
[3] M. O’Neill and C. Ryan, “Grammatical evolution,” IEEE Trans. Evol. Comput., vol. 5, no. 4, pp. 349–358, Aug. 2001.
[4] J. F. Miller and P. Thomson, “Cartesian genetic programming,” in Genetic Programming. Berlin, Germany: Springer, 2000, pp. 121–132.
[5] C. Ferreira, “Gene expression programming: A new adaptive algorithm for solving problems,” Complex Syst., vol. 13, no. 2, pp. 87–129, 2001.
[6] M. F. Brameier and W. Banzhaf, Linear Genetic Programming. New York, NY, USA: Springer, 2007.
[7] C. Zhou, W. Xiao, T. M. Tirpak, and P. C. Nelson, “Evolving accurate and compact classification rules with gene expression programming,” IEEE Trans. Evol. Comput., vol. 7, no. 6, pp. 519–531, Dec. 2003.
[8] C. Ferreira, Gene Expression Programming. Berlin, Germany: Springer, 2006.
[9] N. Sabar, M. Ayob, G. Kendall, and R. Qu, “The automatic design of hyper-heuristic framework with gene expression programming for combinatorial optimization problems,” IEEE Trans. Evol. Comput. [Online]. Available: http://ieeexplore.ieee.org/xpl/articleDetails.jsp?tp=&arnumber=6805577
[10] N. Sabar, M. Ayob, G. Kendall, and R. Qu, “A dynamic multiarmed bandit-gene expression programming hyper-heuristic for combinato-rial optimization problems,” IEEE Trans. Cybern., vol. 45, no. 2, pp. 217–228, Feb. 2015.
[11] J. Zhong, L. Luo, W. Cai, and M. Lees, “Automatic rule identification for agent-based crowd models through gene expression programming,” in Proc. Int. Conf. Auton. Agents Multi-Agent Syst., Saint Paul, MN.
###SL-GEP ###遗传编程 ###差分进化 ###多目标优化 ###结构复杂度
&&&&
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
[21] T. Van Belle and D. H. Ackley, “Code factoring and the evolution of evolvability,” in Proc. Genet. Evol. Comput. Conf., vol. 2, New York, NY, USA, 2002, pp. 1383–1390.
[22] J. A. Walker and J. F. Miller, “The automatic acquisition, evolution and reuse of modules in Cartesian genetic programming,” IEEE Trans. Evol. Comput., vol. 12, no. 4, pp. 397–417, Aug. 2008.
[23] C. Ferreira, “Automatically defined functions in gene expression programming,” in Genetic Systems Programming. Berlin, Germany: Springer, 2006, pp. 21–56.
[24] R. Storn and K. Price, “Differential evolution—A simple and efficient heuristic for global optimization over continuous spaces,” J. Glob. Optim., vol. 11, no. 4, pp. 341–359, 1997.
[25] M. Schmidt and H. Lipson, “Distilling free-form natural laws from”
###基因表达编程 ###遗传编程 ###模因计算 ###进化计算 ###自动函数定义
&&&&
以下是IEEE Transactions on Evolutionary Computation, Vol. 20, No. 1, February 2016中引用的文献列表：

[23] C. Ferreira, "Automatically defined functions in gene expression programming," in Genetic Systems Programming. Berlin, Germany: Springer, 2006, pp. 21–56.
[24] R. Storn and K. Price, "Differential evolution—A simple and efficient heuristic for global optimization over continuous spaces," J. Glob. Optim., vol. 11, no. 4, pp. 341–359, 1997.
[25] M. Schmidt and H. Lipson, "Distilling free-form natural laws from experimental data," Science, vol. 324, no. 5923, pp. 81–85, 2009.
[26] J. McDermott et al., "Genetic programming needs better benchmarks," in Proc. Genet. Evol. Comput. Conf., Philadelphia, PA, USA, 2012, pp. 791–798.
[27] J. Y.-C. Liu, J.-H. A. Chen, C.-T. Chiu, and J.-C. Hsieh, "An extension of gene expression programming with hybrid selection," in Proc. 2nd Int. Conf. Intell. Technol. Eng. Syst. (ICITES), Hong Kong, 2014, pp. 635–641.
[28] Y. Zhang and J. Xiao, "A new strategy for gene expression programming and its applications in function mining," Univ. J. Comput. Sci. Eng. Technol., vol. 1, no. 2, pp. 122–126, 2010.
[29] Y. Peng, C. Yuan, X. Qin, J. Huang, and Y. Shi, "An improved gene expression programming approach for symbolic regression problems," Neurocomputing, vol. 137, pp. 293–301, Aug. 2014.
[30] E. Bautu, A. Bautu, and H. Luchian, "AdaGEP—An adaptive gene expression programming algorithm," in Proc. Int. Symp. Symbol. Numer. Algorithms Sci. Comput. (SYNASC), Timisoara, Romania, 2007, pp. 403–406.
[31] J. Zhang and A. C. Sanderson, "JADE: Adaptive differential evolution with optional external archive," IEEE Trans. Evol. Comput., vol. 13, no. 5, pp. 945–958, Oct. 2009.
[32] Y. Wang, Z. Cai, and Q. Zhang, "Differential evolution with composite trial vector generation strategies and control parameters," IEEE Trans. Evol. Comput., vol. 15, no. 1, pp. 55–66, Feb. 2011.
[33] A. K. Qin and P. N. Suganthan, "Self-adaptive differential evolution algorithm for numerical optimization," in Proc. IEEE Congr. Evol. Comput., vol. 2. Edinburgh, U.K., 2005, pp. 1785–1791.
[34] L. Tang, Y. Dong, and J. Liu, "Differential evolution with an individual-dependent mechanism," IEEE Trans. Evol. Comput. [Online]. Available: http://ieeexplore.ieee.org/xpl/articleDetails.jsp?tp=&arnumber=6913512
[35] A. Lipowski and D. Lipowska, "Roulette-wheel selection via stochastic acceptance," Phys. A, Statist. Mech. Appl., vol. 391, no. 6, pp. 2193–2196, 2012.
[36] C. Ferreira, "Function finding and the creation of numerical constants in gene expression programming," in Advances in Soft Computing. London, U.K.: Springer, 2003, pp. 257–265.
[37] M. Zhang and W. Smart, "Genetic programming with gradient descent search for multiclass object classification," in Genetic Programming. Berlin, Germany: Springer, 2004, pp. 399–408.
[38] M. Kommenda, G. Kronberger, S. Winkler, M. Affenzeller.
###基因表达编程 ###差分进化 ###遗传编程 ###进化计算 ###优化算法
&&&&
以下是关于遗传编程、进化计算和相关优化算法的文献引用。这些引用涵盖了从函数发现、数值常数创建到多类对象分类、常数优化、差分进化、符号回归、调度规则演化以及性能测量可靠性等多个方面。文献中还涉及了遗传算法的统计技术、性能测量以及模块的演化和获取。
###遗传编程 ###进化计算 ###优化算法 ###符号回归 ###差分进化
&&&&
[48] J. A. Walker and J. F. Miller, “Evolution and acquisition of modules in Cartesian genetic programming,” in Genetic Programming. Berlin, Germany: Springer, 2004, pp. 187–197.
[49] G. F. Smits and M. Kotanchek, “Pareto-front exploitation in symbolic regression,” in Genetic Programming Theory and Practice II. New York, NY, USA: Springer, 2005, pp. 283–299.
[50] Z. Huang, “Schema theory for gene expression programming,” Ph.D. dissertation, School of Engineering and Design, Brunel Univ., Uxbridge, U.K., 2014.

Jinghui Zhong received the B.Eng., M.Eng., and Ph.D. degrees from the School of Information Science and Technology, Sun Yat-sen University, Guangzhou, China, in 2005, 2007, and 2012, respectively. He is a Research Fellow with the School of Computer Engineering, Nanyang Technological University, Singapore. His research interests include genetic programming, differential evolution, ant colony optimization, and the applications of evolutionary computations.

Yew-Soon Ong received the B.S. and M.Eng. degrees in electrical and electronics engineering from Nanyang Technological University (NTU), Singapore, in 1998 and 1999, respectively, and the Ph.D. degree in artificial intelligence in complex design from the Computational Engineering and Design Center, University of Southampton, Southampton, U.K., in 2003. He is currently an Associate Professor and the Director of the A*Star SIMTECH-NTU Joint Laboratory on Complex Systems and Programme, School of Computer Engineering, NTU. He is a Principal Investigator of the Rolls-Royce@NTU Corporate Laboratory on Large Scale Data Analytics, Singapore. His research interests include computational intelligence spanning across memetic computation, evolutionary design, machine learning, and big data. His research work on memetic algorithm was featured in the Emerging Research Fronts of the Essential Science Indicators in 2007. Dr. Ong received the 2015 IEEE Computational Intelligence Magazine Outstanding Paper Award and the 2012 IEEE Transactions on Evolutionary Computation Outstanding Paper Award for his published works on memetic computation. He is the Founding Technical Editor-in-Chief of Memetic Computing Journal; the Founding Chief Editor of Studies in Adaptation, Learning, and Optimization (Springer); and an Associate Editor of IEEE Transactions on Evolutionary Computation, IEEE Transactions on Neural Network and Learning Systems, IEEE Computational Intelligence Magazine, IEEE Transactions on Cybernetics, and IEEE Transactions on Big Data.

Wentong Cai received the Ph.D. degree in computer science from University of Exeter, Exeter, U.K., in 1991. He is a Professor with the School of Computer Engineering, Nanyang Technological University, Singapore, where he is also the Director of the Parallel and Distributed Computing Centre. His research interests include modeling and simulation, particularly, modeling and simulation of large-scale systems.
###遗传编程 ###进化计算 ###机器学习 ###大数据 ###智能计算
&&&&
Wentong Cai于1991年在英国埃克塞特大学获得计算机科学博士学位。他目前是新加坡南洋理工大学计算机工程学院的教授，并担任并行与分布式计算中心主任。他的研究兴趣包括建模与仿真，特别是大规模复杂系统的建模与仿真，以及分布式仿真和虚拟环境的系统支持，并行与分布式计算，特别是云计算、网格计算和集群计算。他还是《ACM Transactions on Modeling and Computer Simulation》的副主编和《Future Generation Computer Systems》的编辑。
###Wentong ###Cai ###计算机科学 ###建模与仿真 ###并行与分布式计算 ###南洋理工大学