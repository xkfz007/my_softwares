
// Script for finding files which have a file path over a certain limit

var nMaxSize = parseInt( SearchParms.FilenameCustomParm );

function isValidFileName( strPath, strFileName )
{
	return ( strPath.length + strFileName.length ) > nMaxSize;
}
