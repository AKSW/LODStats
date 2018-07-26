from RDFStatInterface import RDFStatInterface
from lodstats.util.namespace import get_namespace
import lodstats.util.rdf_namespaces
import RDF
import logging

logger = logging.getLogger("lodstats")

class LinkSets(RDFStatInterface):
	global targets, link_properties
	targets={}
	link_properties={}
	
	def __init__(self, results):
		super(LinkSets, self).__init__(results)
		self.usage_count = self.results['usage_count'] = {}
		with open('../config/targets.txt') as f:
			for line in f:
				if( not line.startswith('#') ): # comment lines
					global targets
					(uriPrefix,datasetName,datasetId) = line.split(',')
					targets[uriPrefix.strip()] = [datasetName.strip(),datasetId.strip()]
		with open('../config/link_properties.txt') as f:
			for line in f:
				if( not line.startswith('#') ): # comment lines
					global link_properties
					(propertyUri,shortName) = line.split(',')
					link_properties[propertyUri.strip()] = shortName.strip()

	def count(self, s, p, o, s_blank, o_l, o_blank, statement):
		if not (statement.subject.is_resource and statement.object.is_resource):
			return
        
		subject_ns = get_namespace(s)
		object_ns = get_namespace(o)
        
		if object_ns is None or subject_ns is None:
			return
		global link_properties
		if subject_ns != object_ns and p in link_properties.keys():
			key = LinkSets.LinkSetKey( subject_ns, p, object_ns )
			self.usage_count[key] = self.usage_count.get(key, 0) + 1

	def voidify(self, void_model, dataset):
		namespaces = lodstats.util.rdf_namespaces.RDFNamespaces()
		global targets

		for link_set_key, link_count in self.usage_count.iteritems():
			link_set_subject_pair = targets.get(link_set_key.subject_ns)
			if link_set_subject_pair is None:
				link_set_subject_target=link_set_key.subject_ns
				subjects_target_uri = "http://example.com#" + link_set_subject_target
			else:
				link_set_subject_target = link_set_subject_pair[0]
				subjects_target_uri = link_set_subject_pair[1]
			
			link_set_object_pair = targets.get(link_set_key.object_ns)
			if link_set_object_pair is None:
				link_set_object_target=link_set_key.object_ns
				objects_target_uri = "http://example.com#" + link_set_object_target
			else:
				link_set_object_target = link_set_object_pair[0]
				objects_target_uri =  link_set_object_pair[1]
				
			link_set_predicate = link_set_key.predicate
			global link_properties
			link_set_predicate_alias = link_properties.get(link_set_predicate)
			# the following really should never happen, since we only evaluate predicates in link_properties.keys()
			if link_set_predicate_alias is None:
				link_set_predicate_alias = link_set_predicate
				logger.error("no alias found for " + link_set_predicate)
			
			link_set_uri = "#" + link_set_subject_target + "_" + link_set_predicate_alias + "_" + link_set_object_target
							
			int_datatype_uri = namespaces.get_rdf_namespace("xsd").integer.uri
			link_set_node = RDF.Node()
			statement_link_set_definition = RDF.Statement(link_set_node, namespaces.get_rdf_namespace("rdf").type, namespaces.get_rdf_namespace("void").Linkset)
			statement_linked_triples_value = RDF.Statement(link_set_node, namespaces.get_rdf_namespace("void").triples, RDF.Node(literal=str(link_count), datatype=int_datatype_uri))
			statement_link_predicate = RDF.Statement(link_set_node, namespaces.get_rdf_namespace("void").linkPredicate, RDF.Node(uri_string=link_set_predicate))
			statement_subjects_target = RDF.Statement(link_set_node, namespaces.get_rdf_namespace("void").subjectsTarget, RDF.Node(uri_string=subjects_target_uri))
			statement_objects_target = RDF.Statement(link_set_node, namespaces.get_rdf_namespace("void").objectsTarget, RDF.Node(uri_string=objects_target_uri))
			statement_subset = RDF.Statement(dataset, namespaces.get_rdf_namespace("void").subset, link_set_node );

			void_model.append(statement_link_set_definition)
			void_model.append(statement_linked_triples_value)
			void_model.append(statement_link_predicate)
			void_model.append(statement_subjects_target)
			void_model.append(statement_objects_target)
			void_model.append(statement_subset)
        
        
                    
	def sparql(self, endpoint):
		pass
	
	class LinkSetKey:
		def __init__(self, subject_ns, predicate, object_ns ):
			self.subject_ns = subject_ns
			self.predicate = predicate
			self.object_ns = object_ns
		
		def __attrs(self):
			return( self.subject_ns, self.predicate, self.object_ns )
		
		def __eq__(self, other):
			return isinstance(other, LinkSets.LinkSetKey) and self.__attrs() == other.__attrs()

		def __hash__(self):
			return hash(self.__attrs())
		
		def __str__(self):
			return 'subjectNamespace="'+self.subject_ns+'", predicate="' + self.predicate + '", objectNamespace="' + self.object_ns + '"'