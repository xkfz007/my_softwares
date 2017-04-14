
// This script returns all folders that DO NOT contain a specific 
// file.
	
var objFSO = new ActiveXObject( "Scripting.FileSystemObject" );

function isValidFileName( strPath, strFileName )
{
	// Look to see if a file exists in the folder provided (assumes that
	// this script is only called for folders, ie Attribute - Folders = ON).
	
	var bIsValid = false;
	try
	{
		var strFolderPath = strPath + strFileName;
		bIsValid = !objFSO.FileExists( strFolderPath + "\\" + SearchParms.FilenameCustomParm );
	}
	catch( e )	{}
	return bIsValid;
}