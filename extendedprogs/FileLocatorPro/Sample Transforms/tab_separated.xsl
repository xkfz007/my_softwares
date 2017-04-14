<?xml version="1.0"?>
<!-- Tab separated Transform
    Copyright (C) Mythicsoft Ltd 2012. All rights reserved.
    
    Produces output that contains the path, file name, file size, created, last accessed, last modified date, hit count
    separated by the tab (0x09) character, with each file on a new line.
    -->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
			xmlns:rslt="http://www.mythicsoft.com/FileLocator_16Aug2005"
           version="1.0">

  <xsl:output method="text"/>

  <xsl:template match="/">
    <xsl:apply-templates select="//rslt:file"/>
  </xsl:template>

  <xsl:template match="rslt:file">
    <xsl:value-of select="rslt:path"/>
    <xsl:text>&#09;</xsl:text>
    <xsl:value-of select="rslt:name"/>
    <xsl:text>&#09;</xsl:text>
    <xsl:value-of select="rslt:size"/>
    <xsl:text>&#09;</xsl:text>
    <xsl:value-of select="rslt:type"/>
    <xsl:text>&#09;</xsl:text>
    <xsl:value-of select="rslt:modified"/>
    <xsl:text>&#09;</xsl:text>
    <xsl:value-of select="rslt:lastaccess"/>
    <xsl:text>&#09;</xsl:text>
    <xsl:value-of select="rslt:created"/>
    <xsl:text>&#09;</xsl:text>
    <xsl:value-of select="rslt:contents/@rslt:totalhitcount"/>
    <xsl:text>&#09;</xsl:text>
    <xsl:text>&#13;&#10;</xsl:text>
  </xsl:template>

</xsl:stylesheet>