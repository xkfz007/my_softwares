
var objFSO = new ActiveXObject( "Scripting.FileSystemObject" );

function isValidFileName( strPath, strFileName )
{
	// Open the folder and see if there are any subfolders or files
	// Note: While this script will filter out only folders it is more efficient to
	// have the main search filter them out first by setting the 'Folders = On' attribute
	// in the Attributes tab.
	
	var bIsValid = false;
	try
	{
		var strFolderPath = strPath + strFileName
		
		if ( objFSO.FolderExists( strFolderPath ) )
		{
			var folderCheck = objFSO.GetFolder( strFolderPath );
			bIsValid = ((folderCheck.SubFolders.Count == 0) && (folderCheck.Files.Count == 0));			
		}
	}
	catch( e )	{}
	return bIsValid;
}