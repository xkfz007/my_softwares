<?xml version="1.0"?>
<!-- Generate XCOPY to copy from one drive to another preserving folder structure.
    Copyright (C) Mythicsoft Ltd 2009. All rights reserved.
    
    For each file an XCOPY command is generated with only the drive letter 
	replaced in the source path. e.g.
	c:\folder1\folder2\filename1.txt
	
	generates:
	xcopy "c:\folder1\folder2\filename1.txt" "e:\folder1\folder2\*"
	
	NOTE: Will not work with UNC paths. e.g. \\server1\folder1\folder2
    -->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
			xmlns:rslt="http://www.mythicsoft.com/FileLocator_16Aug2005"
           version="1.0">

  <xsl:output method="text" indent="yes"/>

  <xsl:template match="/">
    <xsl:apply-templates select="//rslt:file"/>
  </xsl:template>

  <xsl:template match="rslt:file">
	<xsl:text>xcopy "</xsl:text>
    <xsl:value-of select="rslt:path"/>
    <xsl:value-of select="rslt:name"/>
    <xsl:text>" "</xsl:text>
    <xsl:text>e:</xsl:text>		<!-- This is the destination drive letter -->
    <xsl:value-of select="substring-after(rslt:path, ':')"/>
    <xsl:text>*"&#13;&#10;</xsl:text>
  </xsl:template>

</xsl:stylesheet>