<?xml version="1.0"?>

<!-- HTML Transform
    Copyright (C) Mythicsoft Ltd 2009. All rights reserved.
    
    An XSLT to generate an HTML version of the FileLocator Pro results.
	Change the parameter 'showcontents' to zero if you don't want contents to be displayed. 
    -->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
			xmlns:rslt="http://www.mythicsoft.com/FileLocator_16Aug2005"
      version="1.0">

  <xsl:output method="html"/>

  <xsl:param name="showfile">1</xsl:param>
  <xsl:param name="showcontents">1</xsl:param>
  <xsl:param name="showsurrounding"></xsl:param>

  <xsl:template match="/">
    <HTML>
      <HEAD>
          <title>FileLocator Pro Results</title>
      </HEAD>
      <body>
		<xsl:apply-templates select="//rslt:file"/>
      </body>
    </HTML>

  </xsl:template>


  <!-- Show file information, highlighting it with bold + underline if we're also
    showing content information -->


  <xsl:template match="rslt:file">
    <xsl:if test="$showfile='1'">

      <xsl:if test="$showcontents='1'">
        <b>
		<a href="{rslt:path}{rslt:name}">
		  <xsl:value-of select="rslt:path"/>
          <xsl:value-of select="rslt:name"/>
		</a>
          <xsl:text> (</xsl:text>
          <xsl:value-of select="rslt:size"/>
          <xsl:text> </xsl:text>
          <xsl:value-of select="rslt:modified"/>
          <xsl:text>) </xsl:text>
        </b>
        <br/>
        <table>
          <xsl:apply-templates select="rslt:contents/rslt:line"/>
        </table>
      </xsl:if>

      <xsl:if test="$showcontents='0'">
		<a href="{rslt:path}{rslt:name}">
		  <xsl:value-of select="rslt:path"/>
          <xsl:value-of select="rslt:name"/>
		</a>
        <xsl:text> (</xsl:text>
        <xsl:value-of select="rslt:size"/>
        <xsl:text> </xsl:text>
        <xsl:value-of select="rslt:modified"/>
        <xsl:text>) </xsl:text>
      </xsl:if>
      <br/>
    </xsl:if>
  </xsl:template>

  <!-- Display information about the line (using a table for formatting) 
    If the line is a found line then use the hit template to actually produce
    the output -->
  
  <xsl:template match="rslt:line">
    <xsl:if test="$showsurrounding='1' or @rslt:linetype='found'">
      <TR>
        <TD width="50">
          <xsl:value-of select="@rslt:number"/>
        </TD>
        <TD>
          <xsl:if test="@rslt:linetype='found'">
            <xsl:apply-templates select="rslt:hit"/>
          </xsl:if>
          <xsl:if test="@rslt:linetype != 'found'">
            <xsl:value-of select="rslt:text"/>
          </xsl:if>
        </TD>
      </TR>
    </xsl:if>
  </xsl:template>


  <!-- Display the line using the hit list information for highlighting 
   (Remember that since the select statement selected a node list which only contained
   'hit' nodes the 'text' node is not included when calculating position() and last() -->
  
  <xsl:template match="rslt:hit">
    <xsl:if test="position()=1">
      <xsl:value-of select="substring(../rslt:text, 1, @rslt:exprstart)"/>
    </xsl:if>
    <b>
      <font color="blue">
        <xsl:value-of select="substring(../rslt:text, @rslt:exprstart + 1, @rslt:exprlength)"/>
      </font>
    </b>

    <!-- If this is not the last in the list of hits then show the following text up to the 
        next hit, otherwise just show the text following this hit -->
    
     <xsl:if test="position()!=last()">
      <xsl:value-of select="substring(../rslt:text, @rslt:exprstart + @rslt:exprlength + 1, following-sibling::rslt:hit[1]/@rslt:exprstart - @rslt:exprstart - @rslt:exprlength)"/>
    </xsl:if>
    <xsl:if test="position()=last()">
      <xsl:value-of select="substring(../rslt:text, @rslt:exprstart + @rslt:exprlength + 1)"/>
    </xsl:if>
  </xsl:template>

</xsl:stylesheet>