
// This script returns all files that exist in the search list and
// a referenced folder
	
var objFSO = new ActiveXObject( "Scripting.FileSystemObject" );

function isValidFileName( strPath, strFileName )
{
	// Look to see if the file exists in the reference folder
	
	var bIsValid = false;
	try
	{
		bIsValid = objFSO.FileExists( SearchParms.FilenameCustomParm + "\\" + strFileName );
	}
	catch( e )	{}
	return bIsValid;
}