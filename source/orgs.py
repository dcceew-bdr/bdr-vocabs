import csv
from rdflib import Graph, URIRef, Literal, BNode, Namespace, XSD, RDF, SKOS, SDO

g = Graph()

cs = URIRef("https://linked.data.gov.au/dataset/bdr/orgs")
ausbn = URIRef("http://id.loc.gov/vocabulary/identifiers/ausbn")

metadata = \
    """
    PREFIX : <https://linked.data.gov.au/dataset/bdr/orgs/>
    PREFIX cs: <https://linked.data.gov.au/dataset/bdr/orgs>
    PREFIX schema: <https://schema.org/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
    cs:
        a skos:ConceptScheme ;
        skos:definition "Organisations known to own & submit data to the Biodiversity Date Repository"@en ;
        skos:historyNote "This vocabulary was developed for the Biodiversity Data Repository and is live in that it grows with new data submissions from new organisations" ;
        skos:prefLabel "BDR Organisations"@en ;
        schema:creator <https://linked.data.gov.au/org/dcceew> ;
        schema:dateCreated "2024-07-09"^^xsd:date ;
        schema:dateModified "2025-08-19"^^xsd:date ;
        schema:license <http://purl.org/NET/rdflicense/cc-by4.0> ;
        schema:publisher <https://linked.data.gov.au/org/dcceew> ;
        skos:hasTopConcept
            <https://linked.data.gov.au/org/birdlife> ,
            <https://linked.data.gov.au/org/tern> ;
    .
    
    <https://linked.data.gov.au/org/birdlife>
        a
            skos:Concept ,
            schema:Organization ;
        skos:definition "Australian Bird science and conservation organisation."@en ;
        skos:historyNote "Added by BDR Admin for the use in the BDR, from AGLDWG Orgs Catalogue https://catalogue.linked.data.gov.au/index.php/org/birdlife" ;
        skos:inScheme cs: ;
        skos:prefLabel "BirdLife Australia"@en ;
        skos:topConceptOf cs: ;
        schema:name "BirdLife Australia" ;
        schema:url "https://birdlife.org.au"^^xsd:anyURI ;
        skos:notation "75 149 124 774"^^<http://id.loc.gov/vocabulary/identifiers/ausbn> ;
    .
    
    <https://linked.data.gov.au/org/tern>
        a
            skos:Concept,
            schema:Organisation ;
        skos:historyNote "From AGLDWG Orgs Catalogue https://catalogue.linked.data.gov.au/index.php/org/tern" ;
        skos:topConceptOf cs: ;
        skos:inScheme cs: ;
        skos:definition "Terrestrial Ecosystems Research Network"@en ;
        skos:prefLabel "Terrestrial Ecosystems Research Network"@en ;
        schema:description "Australia’s land ecosystem observatory." ;
        schema:url "https://tern.org.au"^^xsd:anyURI ;
        schema:name "Terrestrial Ecosystems Research Network" ;
    . 
    """

hn = Literal("Added from data supplied to tne BDR from jurisdictions via https://submit.bdr.gov.au in mid-2025")

with open("orgs.csv") as f:
    for line in sorted(csv.reader(f, delimiter=",", quotechar='"'), key=lambda x: x[3]):
        if line[0] == "Original":
            continue
        iri = URIRef(line[1])
        if len(line[2]) > 1:
            abn = Literal(line[2], datatype=ausbn)
        name = Literal(line[3])
        name_lang = Literal(line[3], lang="en")
        url = Literal(line[4], datatype=XSD.anyURI)

        print(name)

        g.add((iri, RDF.type, SKOS.Concept))
        g.add((iri, RDF.type, SDO.Organization))
        g.add((iri, SKOS.prefLabel, name_lang))
        g.add((iri, SKOS.definition, name_lang))
        g.add((iri, SDO.name, name))
        if len(line[2]) > 1:
            g.add((iri, SKOS.notation, abn))
        g.add((iri, SDO.url, url))
        g.add((iri, SKOS.inScheme, cs))
        g.add((iri, SKOS.topConceptOf, cs))
        g.add((cs, SKOS.hasTopConcept, iri))
        g.add((cs, SKOS.historyNote, hn))

        g.parse(data=metadata, format="turtle")

g.serialize(destination="orgs.ttl", format="longturtle")