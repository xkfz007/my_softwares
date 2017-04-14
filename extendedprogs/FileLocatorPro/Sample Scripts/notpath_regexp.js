
// An example of a NOT expression on a file's pathname
// this time using JScript's built in Regular Expression object.

var regExp = new RegExp( SearchParms.FilenameCustomParm, "i" );

function isValidFileName( strPath, strFileName )
{
	var bIsValid = true;
	try
	{
		bIsValid = !regExp.test( strPath );
	}
	catch( e )	{}
	return bIsValid;
}
