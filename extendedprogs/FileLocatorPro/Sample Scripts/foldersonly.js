
var objFSO = new ActiveXObject( "Scripting.FileSystemObject" );

function isValidFileName( strPath, strFileName )
{
	var bIsValid = false;
	try
	{
		bIsValid = objFSO.FolderExists( strPath + strFileName );
	}
	catch( e )	{}
	return bIsValid;
}