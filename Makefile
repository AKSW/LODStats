RDFDUMP = test/resources/public-spending-in-greece.rdf
BENCHDIR = benchmark

benchmark: benchmark-ClassesDefined benchmark-UsedClasses benchmark-ClassHierarchyDepth benchmark-PropertiesDefined benchmark-PropertyUsage benchmark-PropertyUsageDistinctPerSubject benchmark-PropertyUsageDistinctPerObject benchmark-Outdegree benchmark-Indegree benchmark-PropertyHierarchyDepth benchmark-SubclassUsage benchmark-Entities benchmark-Literals benchmark-BlanksAsSubject benchmark-BlanksAsObject benchmark-Datatypes benchmark-Languages benchmark-StringLength benchmark-TypedSubjects benchmark-LabeledSubjects benchmark-SameAs benchmark-Links benchmark-Vocabularies benchmark-VocabulariesPerNode
	mkdir benchmark

benchmark-ClassesDefined:
	$(eval STAT = ClassesDefined)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

benchmark-UsedClasses:
	$(eval STAT = UsedClasses)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

benchmark-ClassHierarchyDepth:
	$(eval STAT = ClassHierarchyDepth)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

benchmark-PropertiesDefined:
	$(eval STAT = PropertiesDefined)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

benchmark-PropertyUsage:
	$(eval STAT = PropertyUsage)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

benchmark-PropertyUsageDistinctPerSubject:
	$(eval STAT = PropertyUsageDistinctPerSubject)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

benchmark-PropertyUsageDistinctPerObject:
	$(eval STAT = PropertyUsageDistinctPerObject)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

benchmark-Outdegree:
	$(eval STAT = Outdegree)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

benchmark-Indegree:
	$(eval STAT = Indegree)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time
	
benchmark-PropertyHierarchyDepth:
	$(eval STAT = PropertyHierarchyDepth)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time
	
benchmark-SubclassUsage:
	$(eval STAT = SubclassUsage)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time
	
benchmark-Entities:
	$(eval STAT = Entities)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time
	
benchmark-Literals:
	$(eval STAT = Literals)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time
	
benchmark-BlanksAsSubject:
	$(eval STAT = BlanksAsSubject)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time
	
benchmark-BlanksAsObject:
	$(eval STAT = BlanksAsObject)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time
	
benchmark-Datatypes:
	$(eval STAT = Datatypes)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

benchmark-Languages:
	$(eval STAT = Languages)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

benchmark-StringLength:
	$(eval STAT = StringLength)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

benchmark-TypedSubjects:
	$(eval STAT = TypedSubjects)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

benchmark-LabeledSubjects:
	$(eval STAT = LabeledSubjects)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

benchmark-SameAs:
	$(eval STAT = SameAs)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

benchmark-Links:
	$(eval STAT = Links)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

benchmark-Vocabularies:
	$(eval STAT = Vocabularies)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time

benchmark-VocabulariesPerNode:
	$(eval STAT = VocabulariesPerNode)
	{ time lodstats -z $(STAT) $(RDFDUMP) > $(BENCHDIR)/$(STAT).bench.out ; } 2> $(BENCHDIR)/$(STAT).bench.time
