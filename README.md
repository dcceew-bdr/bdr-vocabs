# BDR Vocabularies

Vocabularies created for use specifically with the [Biodiversity Data Repository](https://bdr.gov.au) systems and data.

These vocabularies are presented online as part of the BDR's catalogues of information at:

* **<https://bdr.gov.au>**

Typically, you will want to access these vocabularies from there. This location is only for back-end editing of vocabulary content by BDR Staff.

## License

The data in this repository are licensed for reuse under the [Creative Commons BY 4.0]() license, a copy of the deed of which is within this repository in the `LICENSE` file with the following copyright notice:

&copy; Commonwealth of Australia (Department of Climate Change, Energy, the Environment and Water), 2025

## Contact

These vocabularies are maintained by the BDR Team so please contact them with all enquiries:

**BDR Team**  
_Department of Climate Change, Energy and the Environment (DCCEEW)_  
<https://bdr.gov.au>  
<bdr@dcceew.gov.au>

## Catalogue Technical Details

This catalogue of vocabularies is created as a [Prez Manifest](https://prez.dev/manifest/)-compliant catalogue. The manifest file is `manifest.ttl` and it lists the following resources:

| Resource                                                                                                                                            | Role                                                                                                                | Description                                                                          |
|-----------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Catalogue Definition:<br />[`catalogue.ttl`](catalogue.ttl)                                                                                         | [Catalogue Data](https://prez.dev/ManifestResourceRoles/CatalogueData)                                              | The definition of, and medata for, the container which here is a dcat:Catalog object |
| Resource Data:<br />[`vocabs/*.ttl`](vocabs/*.ttl)                                                                                                  | [Resource Data](https://prez.dev/ManifestResourceRoles/ResourceData)                                                | skos:ConceptScheme objects in RDF (Turtle) files in the vocabs/ folder               |
| Labels:<br />[`labels.ttl`](labels.ttl)                                                                                                             | [Complete Catalogue and Resource Labels](https://prez.dev/ManifestResourceRoles/CompleteCatalogueAndResourceLabels) | An RDF file containing all the labels for the container content                      |