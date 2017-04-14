
// An example of a NOT expression. This will validate that the value appearing in the 'Custom Parm' does
// not appear on the specified line.

function isValidLine( nLineNum, strText )
{
	var bIsValid = true;
	try
	{
		bIsValid = ( strText.indexOf( SearchParms.ContainingTextCustomParm ) < 0 );
	}
	catch( e )	{}
	return bIsValid;
}
