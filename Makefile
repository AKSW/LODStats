RDFDUMP = test/resources/public-spending-in-greece.rdf
BENCHDIR = benchmark

memorybench: memorybench-ClassesDefined memorybench-UsedClasses memorybench-ClassHierarchyDepth memorybench-PropertiesDefined memorybench-PropertyUsage memorybench-PropertyUsageDistinctPerSubject memorybench-PropertyUsageDistinctPerObject memorybench-Outdegree memorybench-Indegree memorybench-PropertyHierarchyDepth memorybench-SubclassUsage memorybench-Entities memorybench-Literals memorybench-BlanksAsSubject memorybench-BlanksAsObject memorybench-Datatypes memorybench-Languages memorybench-StringLength memorybench-TypedSubjects memorybench-LabeledSubjects memorybench-SameAs memorybench-Links memorybench-Vocabularies memorybench-VocabulariesPerNode
	mkdir memorybench
	mv *.dat memorybench

benchmark: benchmark-ClassesDefined benchmark-UsedClasses benchmark-ClassHierarchyDepth benchmark-PropertiesDefined benchmark-PropertyUsage benchmark-PropertyUsageDistinctPerSubject benchmark-PropertyUsageDistinctPerObject benchmark-Outdegree benchmark-Indegree benchmark-PropertyHierarchyDepth benchmark-SubclassUsage benchmark-Entities benchmark-Literals benchmark-BlanksAsSubject benchmark-BlanksAsObject benchmark-Datatypes benchmark-Languages benchmark-StringLength benchmark-TypedSubjects benchmark-LabeledSubjects benchmark-SameAs benchmark-Links benchmark-Vocabularies benchmark-VocabulariesPerNode
	mkdir benchmark

benchmark-ClassesDefined:
	$(eval STAT = ClassesDefined)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

memorybench-ClassesDefined:
	$(eval STAT = ClassesDefined)
	mprof run lodstats -z $(STAT) $(RDFDUMP) 
	mv *.dat memorybench/$(STAT).membench

benchmark-UsedClasses:
	$(eval STAT = UsedClasses)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

memorybench-UsedClasses:
	$(eval STAT = UsedClasses)
	mprof run lodstats -z $(STAT) $(RDFDUMP) 
	mv *.dat memorybench/$(STAT).membench

benchmark-ClassHierarchyDepth:
	$(eval STAT = ClassHierarchyDepth)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

memorybench-ClassHierarchyDepth:
	$(eval STAT = ClassHierarchyDepth)
	mprof run lodstats -z $(STAT) $(RDFDUMP) 
	mv *.dat memorybench/$(STAT).membench

benchmark-PropertiesDefined:
	$(eval STAT = PropertiesDefined)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

memorybench-PropertiesDefined:
	$(eval STAT = PropertiesDefined)
	mprof run lodstats -z $(STAT) $(RDFDUMP) 
	mv *.dat memorybench/$(STAT).membench

benchmark-PropertyUsage:
	$(eval STAT = PropertyUsage)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

memorybench-PropertyUsage:
	$(eval STAT = PropertyUsage)
	mprof run lodstats -z $(STAT) $(RDFDUMP) 
	mv *.dat memorybench/$(STAT).membench

benchmark-PropertyUsageDistinctPerSubject:
	$(eval STAT = PropertyUsageDistinctPerSubject)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

memorybench-PropertyUsageDistinctPerSubject:
	$(eval STAT = PropertyUsageDistinctPerSubject)
	mprof run lodstats -z $(STAT) $(RDFDUMP) 
	mv *.dat memorybench/$(STAT).membench

benchmark-PropertyUsageDistinctPerObject:
	$(eval STAT = PropertyUsageDistinctPerObject)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

memorybench-PropertyUsageDistinctPerObject:
	$(eval STAT = PropertyUsageDistinctPerObject)
	mprof run lodstats -z $(STAT) $(RDFDUMP) 
	mv *.dat memorybench/$(STAT).membench

benchmark-Outdegree:
	$(eval STAT = Outdegree)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

memorybench-Outdegree:
	$(eval STAT = Outdegree)
	mprof run lodstats -z $(STAT) $(RDFDUMP) 
	mv *.dat memorybench/$(STAT).membench

benchmark-Indegree:
	$(eval STAT = Indegree)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

memorybench-Indegree:
	$(eval STAT = Indegree)
	mprof run lodstats -z $(STAT) $(RDFDUMP) 
	mv *.dat memorybench/$(STAT).membench
	
benchmark-PropertyHierarchyDepth:
	$(eval STAT = PropertyHierarchyDepth)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

memorybench-PropertyHierarchyDepth:
	$(eval STAT = PropertyHierarchyDepth)
	mprof run lodstats -z $(STAT) $(RDFDUMP) 
	mv *.dat memorybench/$(STAT).membench
	
benchmark-SubclassUsage:
	$(eval STAT = SubclassUsage)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

memorybench-SubclassUsage:
	$(eval STAT = SubclassUsage)
	mprof run lodstats -z $(STAT) $(RDFDUMP) 
	mv *.dat memorybench/$(STAT).membench
	
benchmark-Entities:
	$(eval STAT = Entities)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

memorybench-Entities:
	$(eval STAT = Entities)
	mprof run lodstats -z $(STAT) $(RDFDUMP) 
	mv *.dat memorybench/$(STAT).membench
	
benchmark-Literals:
	$(eval STAT = Literals)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

memorybench-Literals:
	$(eval STAT = Literals)
	mprof run lodstats -z $(STAT) $(RDFDUMP) 
	mv *.dat memorybench/$(STAT).membench
	
benchmark-BlanksAsSubject:
	$(eval STAT = BlanksAsSubject)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

memorybench-BlanksAsSubject:
	$(eval STAT = BlanksAsSubject)
	mprof run lodstats -z $(STAT) $(RDFDUMP) 
	mv *.dat memorybench/$(STAT).membench
	
benchmark-BlanksAsObject:
	$(eval STAT = BlanksAsObject)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

memorybench-BlanksAsObject:
	$(eval STAT = BlanksAsObject)
	mprof run lodstats -z $(STAT) $(RDFDUMP) 
	mv *.dat memorybench/$(STAT).membench
	
benchmark-Datatypes:
	$(eval STAT = Datatypes)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

memorybench-Datatypes:
	$(eval STAT = Datatypes)
	mprof run lodstats -z $(STAT) $(RDFDUMP) 
	mv *.dat memorybench/$(STAT).membench

benchmark-Languages:
	$(eval STAT = Languages)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

memorybench-Languages:
	$(eval STAT = Languages)
	mprof run lodstats -z $(STAT) $(RDFDUMP) 
	mv *.dat memorybench/$(STAT).membench

benchmark-StringLength:
	$(eval STAT = StringLength)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

memorybench-StringLength:
	$(eval STAT = StringLength)
	mprof run lodstats -z $(STAT) $(RDFDUMP) 
	mv *.dat memorybench/$(STAT).membench

benchmark-TypedSubjects:
	$(eval STAT = TypedSubjects)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

memorybench-TypedSubjects:
	$(eval STAT = TypedSubjects)
	mprof run lodstats -z $(STAT) $(RDFDUMP) 
	mv *.dat memorybench/$(STAT).membench

benchmark-LabeledSubjects:
	$(eval STAT = LabeledSubjects)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

memorybench-LabeledSubjects:
	$(eval STAT = LabeledSubjects)
	mprof run lodstats -z $(STAT) $(RDFDUMP) 
	mv *.dat memorybench/$(STAT).membench

benchmark-SameAs:
	$(eval STAT = SameAs)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

memorybench-SameAs:
	$(eval STAT = SameAs)
	mprof run lodstats -z $(STAT) $(RDFDUMP) 
	mv *.dat memorybench/$(STAT).membench

benchmark-Links:
	$(eval STAT = Links)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

memorybench-Links:
	$(eval STAT = Links)
	mprof run lodstats -z $(STAT) $(RDFDUMP) 
	mv *.dat memorybench/$(STAT).membench

benchmark-Vocabularies:
	$(eval STAT = Vocabularies)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

memorybench-Vocabularies:
	$(eval STAT = Vocabularies)
	mprof run lodstats -z $(STAT) $(RDFDUMP) 
	mv *.dat memorybench/$(STAT).membench

benchmark-VocabulariesPerNode:
	$(eval STAT = VocabulariesPerNode)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

memorybench-VocabulariesPerNode:
	$(eval STAT = VocabulariesPerNode)
	mprof run lodstats -z $(STAT) $(RDFDUMP) 
	mv *.dat memorybench/$(STAT).membench
