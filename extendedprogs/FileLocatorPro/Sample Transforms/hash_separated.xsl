<?xml version="1.0"?>
<!-- Hash separated Transform
    Copyright (C) Mythicsoft Ltd 2008. All rights reserved.
    
    Produces output that contains the path, file name, file size, and last modified date
    separated by the '#' character, with each file on a new line.
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
    <xsl:text>#</xsl:text>
    <xsl:value-of select="rslt:name"/>
    <xsl:text>#</xsl:text>
    <xsl:value-of select="rslt:size"/>
    <xsl:text>#</xsl:text>
    <xsl:value-of select="rslt:modified"/>
    <xsl:text>#</xsl:text>
    <xsl:value-of select="rslt:contents/@rslt:totalhitcount"/>
    <xsl:text>#</xsl:text>
    <xsl:text>&#13;&#10;</xsl:text>
  </xsl:template>

</xsl:stylesheet>