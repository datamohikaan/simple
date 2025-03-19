from pathlib import Path
from lxml import etree
from xml.sax.saxutils import escape


class PowerDesignerLDMPreprocessor:
    def preprocess_ldm(self, file_name: str) -> bool:
        file_path = Path(file_name)
        if not file_path.is_file:
            print(f"{file_name} is not a valid file.")
            return False
        # Read the file in memory
        xml_doc: etree.ElementTree = etree.parse(file_path)
        prefix_map = {"c": "collection", "a": "attribute", "o": "object"}
        # Now process all extend attribute text elements
        xml_doc = self.__formalize_extended_attributes(xml_doc, prefix_map)
        # save modified document to new file
        with open(
            file_name[0 : len(file_name) - 4] + "_preprocessed.ldm", "wb"
        ) as xml_out:
            xml_doc.write(
                xml_out, encoding="utf-8", xml_declaration=True, pretty_print=True
            )
        return True

    def __formalize_extended_attributes(
        self, xml_doc: etree.ElementTree, prefix_map: dict
    ) -> etree.ElementTree:
        """
        In a PowerDesigner XML file, Extended attributes are stored in a proprietary format that looks like the example below.
        The content is structured as follows:
        {Guid-of-extension}, name-of-extension, length-of-extension-content=<extension_content>
        where extension content is build from one or more occurences of:
        {guid-of-attribute}, name-of-attibute, length-of-attribute-content=attribute-content

        Example of extended attributes contents:

        <a:ExtendedAttributesText>{4202E4F4-4187-47CE-83BE-51088F229451},TestExtension,155={DA1CC8BE-C80A-4B74-BB79-10F50BE06CBC},TestBooleanField,4=true
            {18ECABD7-88E7-4D0E-8107-0382CDF1E4D3},TestTextField,33=This is test text
            with a newline

            {2ABE46A1-ED92-45C8-B191-7C85DD336346},AnotherTestExtension,222={A2A57166-AB6A-4776-867B-95E7775EFC9F},SecondTestFromAnotherExtension,2=23
            {49F389E0-A1B2-4FFB-BEF1-57FA2A8EBA45},TestFromAnotherExtension,9=4/24/2023
            {C1179E53-39F4-461A-9349-EFF754344DD5},ThirdTestField,10=test third

            {8D660A8B-DD11-4310-A56E-DA20411AD4A3},LocalExtension,215={95993098-3FA0-4867-AE7B-29EA684DE890},TestFieldFromLocal,14=LocalTestValue
            {BAB78320-A5AD-4B8F-83C2-82A3D0C20463},TestFieldFromLocal2,6=test 2
            {D3EC740E-9AE6-46B4-AC99-4EC31FFB1AD8},TestFieldFromLocal3,6=test 3

        </a:ExtendedAttributesText>

        In the example there is a Extension named TestExtension, identified bij guid {4202E4F4-4187-47CE-83BE-51088F229451}. The total length of the content of the extended attributes belonging to this extension = 155.
        As part of this content the extended attribute TestTextField with guid {18ECABD7-88E7-4D0E-8107-0382CDF1E4D3} is included, the content length of this extended attribute = 33 and consists of the text:
        "
        This is test text
        with a newline
        "
        which has a length of 33 characters in the original PowerDesigner model file (including newline and excluding the whitespace that is added here in the example for layout)
        """

        extended_attributes = xml_doc.findall("//a:ExtendedAttributesText", prefix_map)
        for extended_attribute in extended_attributes:
            # get the XML representation for the extended attribute text
            extended_attribute_xml: str = self.__get_xml_representation(
                extended_attribute.text
            )
            # create a etree object using this xml representation
            ext_attr_tree: etree.ElementTree = etree.fromstring(extended_attribute_xml)
            # append the new object to the parent of the extended attributes text element
            extended_attribute.getparent().append(ext_attr_tree)
        return xml_doc

    def __get_xml_representation(self, extended_attribute_text: str) -> str:
        # Define namespaces on the upper element to prevent errors when including the element to the existing tree
        xml_rep: str = (
            '<c:ExtendedAttributes_formalized xmlns:a="attribute" xmlns:c="collection" xmlns:o="object">'
        )
        # replace \n with \r\n since this is what length in the PD file is based on
        extended_attribute_text = extended_attribute_text.replace("\n", "\r\n")
        extension_sections = self.__get_extended_attribute_sections(
            extended_attribute_text
        )
        for section in extension_sections:
            xml_rep = (
                xml_rep
                + f"<c:OriginatingExtension id=\"{section['id']}\" name=\"{section['name']}\">"
            )
            section_attributes = self.__get_extended_attribute_sections(
                section["content"]
            )
            for attribute in section_attributes:
                xml_rep = (
                    xml_rep
                    + f"<a:ExtendedAttribute id=\"{attribute['id']}\" name=\"{attribute['name']}\">"
                )
                xml_rep = xml_rep + escape(attribute["content"])
                xml_rep = xml_rep + "</a:ExtendedAttribute>"
            xml_rep = xml_rep + "</c:OriginatingExtension>"
        xml_rep = xml_rep + "</c:ExtendedAttributes_formalized>"
        return xml_rep

    def __get_extended_attribute_sections(self, attribute_text: str) -> dict:
        # set all to be remaining
        attribute_text_remainder = attribute_text
        sections = []

        # process sections found while there is still text remaining
        while attribute_text_remainder.replace(",", "").strip():
            attribute_text_parts = attribute_text_remainder.split(",")
            section_id: str = attribute_text_parts[0].strip()
            section_name: str = attribute_text_parts[1]
            section_length: int = int(attribute_text_parts[2].split("=", maxsplit=1)[0])
            section_content_start = attribute_text_parts[2].split("=", maxsplit=1)[1]
            attribute_text_remainder = (
                section_content_start
                + ","
                + ",".join(attribute_text_parts[3 : len(attribute_text_parts)])
            )
            section_content = attribute_text_remainder[0:section_length]
            attribute_text_remainder = attribute_text_remainder[section_length + 1 :]
            sections.append(
                {"id": section_id, "name": section_name, "content": section_content}
            )
        return sections
