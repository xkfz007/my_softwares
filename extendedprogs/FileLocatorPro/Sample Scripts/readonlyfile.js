
var objFSO = new ActiveXObject( "Scripting.FileSystemObject" );

function isValidFileName( strPath, strFileName )
{
	var bIsValid = false;
	try
	{
		var objFile = objFSO.GetFile( strPath + strFileName );
		bIsValid = ( objFile.Attributes & 1 );		// Is Read-only?
		
		// Other attributes:
		// Normal = 0
		// ReadOnly = 1
		// Hidden = 2
		// System = 4
		// Volume = 8
		// Directory = 16
		// Archive = 32
		// Alias = 64
		// Compressed = 128
		// 
		// Therefore if you wanted to search for just files with Archive
		// attribute specified you would use something like:
		// bIsValid = (objFile.Attributes & 32 );
	}
	catch( e )	{}
	return bIsValid;
}
