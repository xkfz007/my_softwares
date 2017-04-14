<?xml version="1.0"?>
<!-- Hits only Transform
    Copyright (C) Mythicsoft Ltd 2008. All rights reserved.
    
    Produces output that contains just the hits found in a search, i.e. without any file information
    or extra found text information. Useful for regular expression searches to output text that
    matches a given expression, e.g. extracting telephone numbers, or email addresses.
	
	This transform differs from hits_only.xsl by only outputing the unique hits, i.e. it only outputs the
	value of the hit once regardless of how many times it may actually be found.
    -->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
			xmlns:rslt="http://www.mythicsoft.com/FileLocator_16Aug2005"
           version="1.0">

  <xsl:output method="text" indent="yes"/>
  <xsl:key name="hits-value" match="rslt:hit" use="substring(../rslt:text, @rslt:exprstart + 1, @rslt:exprlength)" />


  <xsl:template match="/">
    <xsl:apply-templates select="//rslt:hit"/>
  </xsl:template>

  <xsl:template match="rslt:hit">
  	<xsl:if test="generate-id() = generate-id(key('hits-value', substring(../rslt:text, @rslt:exprstart + 1, @rslt:exprlength)))">      
    	<xsl:value-of select="substring(../rslt:text, @rslt:exprstart + 1, @rslt:exprlength)"/>
    	<xsl:text>&#13;&#10;</xsl:text>
    </xsl:if>
  </xsl:template>

</xsl:stylesheet>