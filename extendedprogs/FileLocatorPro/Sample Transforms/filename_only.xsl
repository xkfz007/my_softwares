<?xml version="1.0"?>
<!-- Filename only Transform
    Copyright (C) Mythicsoft Ltd 2008. All rights reserved.
    
    Produces output that contains just the file name (without the path), each on a new line.
    -->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
			xmlns:rslt="http://www.mythicsoft.com/FileLocator_16Aug2005"
           version="1.0">

  <xsl:output method="text" indent="yes"/>

  <xsl:template match="/">
    <xsl:apply-templates select="//rslt:file"/>
  </xsl:template>

  <xsl:template match="rslt:file">
    <xsl:value-of select="rslt:name"/>
    <xsl:text>&#13;&#10;</xsl:text>
  </xsl:template>

</xsl:stylesheet>