import RDF

import logging
import lodstats.config
import lodstats.stats
import lodstats.util.interfaces
import lodstats.util.rdf_namespaces

import csv2rdf.ckan.resource
import csv2rdf.ckan.package

logger = logging.getLogger("lodstats")

class MakeVoid(lodstats.util.interfaces.UriParserInterface):
    def __init__(self, rdf_stats, serialize_as="ntriples"):
        self.rdf_stats = rdf_stats
        self.stats_results = rdf_stats.get_stats_results()
        self.uri = rdf_stats.uri
        self.filename = self.identify_filename(self.uri)
        self.serialize_as = serialize_as
        self.namespaces = lodstats.util.rdf_namespaces.RDFNamespaces()

    def ckan_lookup(self):
        #look up meta data from CKAN instance (datahub.io)
        searcher = csv2rdf.ckan.resource.Resource('')
        ckan_resource = searcher.search_by_uri(self.uri)
        if(not ckan_resource):
            return ([], [])
        else:
            searcher = csv2rdf.ckan.resource.Resource(ckan_resource['id'])
            searcher.revision_id = ckan_resource['revision_id']
            ckan_package_name = searcher.request_package_name()
            ckan_package = csv2rdf.ckan.package.Package(ckan_package_name)
            return (ckan_package, ckan_resource)

    def generate_general_void_metadata(self, void_model, void_dataset_entity):
        #source
        void_source = self.rdf_stats.uri
        void_source_entity = RDF.Uri(void_source)
        void_model.append(RDF.Statement(void_dataset_entity,self.namespaces.get_rdf_namespace('dcterms').source,void_source_entity))

        (package, resource) = self.ckan_lookup()
        if(not package):
            logger.info("No general metadata information available!")
        else:
            #foaf:homepage
            foaf_homepage = package.url
            foaf_homepage_entity = RDF.Uri(foaf_homepage)
            void_model.append(RDF.Statement(void_dataset_entity,
                                            self.namespaces.get_rdf_namespace('foaf').homepage,
                                            foaf_homepage_entity))
            #dcterms:title
            dcterms_title = resource['name']
            dcterms_title_entity = RDF.Node(literal=dcterms_title,
                                            datatype=self.namespaces.get_rdf_namespace('xsd').string.uri)
            void_model.append(RDF.Statement(void_dataset_entity,
                                            self.namespaces.get_rdf_namespace('dcterms').title,
                                            dcterms_title_entity))
            #dcterms:description
            dcterms_description = package.notes_rendered
            dcterms_description_entity = RDF.Node(literal=dcterms_description,
                                                  datatype=self.namespaces.get_rdf_namespace('xsd').string.uri)
            void_model.append(RDF.Statement(void_dataset_entity,
                                            self.namespaces.get_rdf_namespace('dcterms').description,
                                            dcterms_description_entity))
            #dcterms:created
            dcterms_created = resource['created']
            dcterms_created_entity = RDF.Node(literal=dcterms_created,
                                              datatype=self.namespaces.get_rdf_namespace('xsd').dateTime.uri)
            void_model.append(RDF.Statement(void_dataset_entity,
                                            self.namespaces.get_rdf_namespace('dcterms').created,
                                            dcterms_created_entity))
            #dcterms:modified
            dcterms_modified = resource['last_modified']
            dcterms_modified_entity = RDF.Node(literal=dcterms_modified,
                                              datatype=self.namespaces.get_rdf_namespace('xsd').dateTime.uri)
            void_model.append(RDF.Statement(void_dataset_entity,
                                            self.namespaces.get_rdf_namespace('dcterms').modified,
                                            dcterms_modified_entity))

            #dcterms:creator
            creator_node = RDF.Node(blank="creator")
            dcterms_creator = package.author
            dcterms_creator_entity = RDF.Node(literal=dcterms_creator,
                                              datatype=self.namespaces.get_rdf_namespace('xsd').string.uri)
            void_model.append(RDF.Statement(creator_node,
                                            self.namespaces.get_rdf_namespace('rdfs').label,
                                            dcterms_creator_entity))

            foaf_mbox_creator = package.author_email
            foaf_mbox_creator_entity = RDF.Node(literal=foaf_mbox_creator,
                                                datatype=self.namespaces.get_rdf_namespace('xsd').string.uri)
            void_model.append(RDF.Statement(creator_node,
                                            self.namespaces.get_rdf_namespace('foaf').mbox,
                                            foaf_mbox_creator_entity))
            void_model.append(RDF.Statement(void_dataset_entity,
                                            self.namespaces.get_rdf_namespace('dcterms').creator,
                                            creator_node))

            #dcterms:publisher (maintainer)
            publisher_node = RDF.Node(blank="publisher")
            dcterms_publisher = package.maintainer
            dcterms_publisher_entity = RDF.Node(literal=dcterms_publisher,
                                              datatype=self.namespaces.get_rdf_namespace('xsd').string.uri)
            void_model.append(RDF.Statement(publisher_node,
                                            self.namespaces.get_rdf_namespace('rdfs').label,
                                            dcterms_publisher_entity))

            foaf_mbox_publisher = package.author_email
            foaf_mbox_publisher_entity = RDF.Node(literal=foaf_mbox_publisher,
                                                datatype=self.namespaces.get_rdf_namespace('xsd').string.uri)
            void_model.append(RDF.Statement(publisher_node,
                                            self.namespaces.get_rdf_namespace('foaf').mbox,
                                            foaf_mbox_publisher_entity))
            void_model.append(RDF.Statement(void_dataset_entity,
                                            self.namespaces.get_rdf_namespace('dcterms').publisher,
                                            publisher_node))

            #package.isopen #True/False - open license?
            dcterms_license = package.license_id #TODO get license uri by license id
            dcterms_license_entity = RDF.Node(literal=dcterms_license,
                                              datatype=self.namespaces.get_rdf_namespace('xsd').string.uri)
            void_model.append(RDF.Statement(void_dataset_entity,
                                            self.namespaces.get_rdf_namespace('dcterms').license,
                                            dcterms_license_entity))

    def get_serializer(self):
        serializer = RDF.Serializer(name=self.serialize_as)
        serializer.set_namespace("rdf", self.namespaces.get_namespace('rdf'))
        serializer.set_namespace("void", self.namespaces.get_namespace('void'))
        serializer.set_namespace("void-ext", self.namespaces.get_namespace('void_ext'))
        serializer.set_namespace("qb", self.namespaces.get_namespace('qb'))
        serializer.set_namespace("dcterms", self.namespaces.get_namespace('dcterms'))
        serializer.set_namespace("ls-void", self.namespaces.get_namespace('ls_void'))
        serializer.set_namespace("ls-qb", self.namespaces.get_namespace('ls_qb'))
        serializer.set_namespace("ls-cr", self.namespaces.get_namespace('ls_cr'))
        serializer.set_namespace("xsd", self.namespaces.get_namespace('xsd'))
        serializer.set_namespace("xstats", self.namespaces.get_namespace('stats'))
        serializer.set_namespace("foaf", self.namespaces.get_namespace('foaf'))
        serializer.set_namespace("rdfs", self.namespaces.get_namespace('rdfs'))
        return serializer

    def qbify(self):
        #not implemented yet
        # qb dataset
        lodstats_qb_dataset_label = "LODStats DataCube Dataset"
        lodstats_qb_dataset_label_node = RDF.Node(literal=lodstats_qb_dataset_label, datatype=ns_xsd.string.uri)
        void_model.append(RDF.Statement(ns_ls_qb.LODStats, ns_rdf.type, ns_qb.Dataset))
        void_model.append(RDF.Statement(ns_ls_qb.LODStats, ns_qb.structure, ns_ls_qb.LODStatsStructure))
        void_model.append(RDF.Statement(ns_ls_qb.LODStats, ns_rdf.label, lodstats_qb_dataset_label_node))

        #qb datastructure
        lodstats_qb_dsd_label = "LODStats DataCube Structure Definition"
        lodstats_qb_dsd_label_node = RDF.Node(literal=lodstats_qb_dsd_label, datatype=ns_xsd.string.uri)
        void_model.append(RDF.Statement(ns_ls_qb.LODStatsStructure, ns_rdf.type, ns_qb.DataStructureDefinition))
        void_model.append(RDF.Statement(ns_ls_qb.LODStatsStructure, ns_qb.component, ns_ls_qb.timeOfMeasureSpec))
        void_model.append(RDF.Statement(ns_ls_qb.LODStatsStructure, ns_qb.component, ns_ls_qb.sourceDatasetSpec))
        void_model.append(RDF.Statement(ns_ls_qb.LODStatsStructure, ns_qb.component, ns_ls_qb.statisticalCriterionSpec))
        void_model.append(RDF.Statement(ns_ls_qb.LODStatsStructure, ns_qb.component, ns_ls_qb.valueSpec))
        void_model.append(RDF.Statement(ns_ls_qb.LODStatsStructure, ns_qb.component, ns_ls_qb.unitSpec))
        void_model.append(RDF.Statement(ns_ls_qb.LODStatsStructure, ns_qb.component, lodstats_qb_dsd_label_node))

        #qb components
        timeOfMeasureSpec_label = "Time of Measure (Component Specification)"
        timeOfMeasureSpec_label_node = RDF.Node(literal=timeOfMeasureSpec_label, datatype=ns_xsd.string.uri)
        void_model.append(RDF.Statement(ns_ls_qb.timeOfMeasureSpec, ns_rdf.type, ns_qb.ComponentSpecification))
        void_model.append(RDF.Statement(ns_ls_qb.timeOfMeasureSpec, ns_qb.dimension, ns_ls_qb.timeOfMeasure))
        void_model.append(RDF.Statement(ns_ls_qb.timeOfMeasureSpec, ns_rdf.label, timeOfMeasureSpec_label_node))

        sourceDatasetSpec_label = "Source Dataset which is observerd (Component Specification)"
        sourceDatasetSpec_label_node = RDF.Node(literal=sourceDatasetSpec_label, datatype=ns_xsd.string.uri)
        void_model.append(RDF.Statement(ns_ls_qb.sourceDatasetSpec, ns_rdf.type, ns_qb.ComponentSpecification))
        void_model.append(RDF.Statement(ns_ls_qb.sourceDatasetSpec, ns_qb.dimension, ns_ls_qb.sourceDataset))
        void_model.append(RDF.Statement(ns_ls_qb.sourceDatasetSpec, ns_rdf.label, sourceDatasetSpec_label_node))

        statisticalCriterionSpec_label = "Statistical Criterion (Component Specification)"
        statisticalCriterionSpec_label_node = RDF.Node(literal=statisticalCriterionSpec_label, datatype=ns_xsd.string.uri)
        void_model.append(RDF.Statement(ns_ls_qb.statisticalCriterionSpec, ns_rdf.type, ns_qb.ComponentSpecification))
        void_model.append(RDF.Statement(ns_ls_qb.statisticalCriterionSpec, ns_qb.dimension, ns_ls_qb.statisticalCriterion))
        void_model.append(RDF.Statement(ns_ls_qb.statisticalCriterionSpec, ns_rdf.label, statisticalCriterionSpec_label_node))

        valueSpec_label = "Measure of Observation (Component Specification)"
        valueSpec_label_node = RDF.Node(literal=valueSpec_label, datatype=ns_xsd.string.uri)
        void_model.append(RDF.Statement(ns_ls_qb.valueSpec, ns_rdf.type, ns_qb.ComponentSpecification))
        void_model.append(RDF.Statement(ns_ls_qb.valueSpec, ns_qb.measure, ns_ls_qb.value))
        void_model.append(RDF.Statement(ns_ls_qb.valueSpec, ns_rdf.label, valueSpec_label_node))

        unitSpec_label = "Unit of Measure (Component Specification)"
        unitSpec_label_node = RDF.Node(literal=unitSpec_label, datatype=ns_xsd.string.uri)
        void_model.append(RDF.Statement(ns_ls_qb.unitSpec, ns_rdf.type, ns_qb.ComponentSpecification))
        void_model.append(RDF.Statement(ns_ls_qb.unitSpec, ns_qb.attribute, ns_ls_qb.unit))
        void_model.append(RDF.Statement(ns_ls_qb.unitSpec, ns_rdf.label, unitSpec_label_node))

        # dimention properties
        timeOfMeasure_label = "Time of Measure"
        timeOfMeasure_label_node = RDF.Node(literal=timeOfMeasure_label, datatype=ns_xsd.string.uri)
        void_model.append(RDF.Statement(ns_ls_qb.timeOfMeasure, ns_rdf.type, ns_qb.DimensionProperty))
        void_model.append(RDF.Statement(ns_ls_qb.timeOfMeasure, ns_rdf.label, timeOfMeasure_label_node))

        sourceDataset_label = "Source Dataset"
        sourceDataset_label_node = RDF.Node(literal=sourceDataset_label, datatype=ns_xsd.string.uri)
        void_model.append(RDF.Statement(ns_ls_qb.sourceDataset, ns_rdf.type, ns_qb.DimensionProperty))
        void_model.append(RDF.Statement(ns_ls_qb.sourceDataset, ns_rdf.label, sourceDataset_label_node))

        statisticalCriterion_label = "Statistical Criterion"
        statisticalCriterion_label_node = RDF.Node(literal=statisticalCriterion_label, datatype=ns_xsd.string.uri)
        void_model.append(RDF.Statement(ns_ls_qb.statisticalCriterion, ns_rdf.type, ns_qb.DimensionProperty))
        void_model.append(RDF.Statement(ns_ls_qb.statisticalCriterion, ns_rdf.label, statisticalCriterion_label_node))

        value_label = "Measure of Observation"
        value_label_node = RDF.Node(literal=value_label, datatype=ns_xsd.string.uri)
        void_model.append(RDF.Statement(ns_ls_qb.value, ns_rdf.type, ns_qb.MeasureProperty))
        void_model.append(RDF.Statement(ns_ls_qb.value, ns_rdf.label, value_label_node))

        unit_label = "Unit of Measure"
        unit_label_node = RDF.Node(literal=unit_label, datatype=ns_xsd.string.uri)
        void_model.append(RDF.Statement(ns_ls_qb.unit, ns_rdf.type, ns_qb.AttributeProperty))
        void_model.append(RDF.Statement(ns_ls_qb.unit, ns_rdf.label, unit_label_node))

        StatisticalCriterion_label = "Statistical Criterion"
        StatisticalCriterion_label_node = RDF.Node(literal=StatisticalCriterion_label, datatype=ns_xsd.string.uri)
        void_model.append(RDF.Statement(ns_ls_qb.StatisticalCriterion, ns_rdf.type, ns_qb.AttributeProperty))
        void_model.append(RDF.Statement(ns_ls_qb.StatisticalCriterion, ns_rdf.label, StatisticalCriterion_label_node))

        # voidify results from custom stats
        #for stat in lodstats.stats.stats_to_do:
            #stat.qbify(void_model, dataset_entity)

        # void:observation extension stuff
        #void_model.append(RDF.Statement(ns_stats.value, ns_rdf.type, ns_qb.MeasureProperty))
        #void_model.append(RDF.Statement(ns_stats.subjectsOfType, ns_rdf.type, ns_qb.DimensonProperty))
        #void_model.append(RDF.Statement(ns_stats.schema, ns_rdf.type, ns_qb.AttributeProperty))

        #serializer.set_namespace("thisdataset", dataset_ns._prefix)

    def voidify(self):
        """present stats in VoID (http://www.w3.org/TR/void/)"""
        serializer = self.get_serializer()

        ###########################
        # VoID dataset definition #
        ###########################
        void_model = RDF.Model()

        void_dataset_uri = self.namespaces.get_namespace('ls_void') + "?source=" + self.rdf_stats.uri #TODO: URI encode ?
        void_dataset_entity = RDF.Uri(void_dataset_uri)

        void_model.append(RDF.Statement(void_dataset_entity,
                                        self.namespaces.get_rdf_namespace("rdf").type,
                                        self.namespaces.get_rdf_namespace("void").Dataset))

        #self.generate_general_void_metadata(void_model, void_dataset_entity)

        #Number of triples
        number_of_triples_node = RDF.Node(literal=str(self.rdf_stats.get_no_of_triples()),
                                          datatype=self.namespaces.get_rdf_namespace("xsd").integer.uri)
        void_model.append(RDF.Statement(void_dataset_entity,
                                        self.namespaces.get_rdf_namespace("void").triples,
                                        number_of_triples_node))

        # voidify results from custom stats
        for stat in lodstats.stats.stats_to_do:
            stat.voidify(void_model, void_dataset_entity)

        return serializer.serialize_model_to_string(void_model)

if __name__ == "__main__":
    import lodstats.RDFStats
    uri = "http://www.gutenberg.org/ebooks/12345.rdf"
    #uri = "http://bio2rdf.org/rdfxml/genbank:BC062795"
    #uri = lodstats.config.rdf_test_file_uri
    stats = lodstats.stats.void_stats
    rdf_stats = lodstats.RDFStats(uri, stats=stats)
    rdf_stats.disable_debug()
    rdf_stats.start_statistics()
    mv = MakeVoid(rdf_stats, serialize_as="turtle")
    print mv.voidify()
