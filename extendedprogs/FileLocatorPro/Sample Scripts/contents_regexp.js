
// An example using JScript's built in Regular Expression object.


var regExp = new RegExp( SearchParms.ContainingTextCustomParm, "i" );

function isValidLine( nLineNum, strText )
{
	var bIsValid = true;
	try
	{
		bIsValid = regExp.test( strText );
	}
	catch( e )	{}
	return bIsValid;
}
