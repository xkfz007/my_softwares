
' An example of a NOT expression on a file's pathname
' using VBScript's built in Regular Expression object.

Dim regEx
Set regEx = new RegExp
regEx.Pattern = SearchParms.FileNameCustomParm
regEx.IgnoreCase = True

Public Function isValidFileName( ByVal strPath, ByVal strFileName )

On Error Resume Next

	Dim bIsValid
	bIsValid = True
	bIsValid = Not regEx.Test( strPath )
	
	isValidFileName = bIsValid

End Function
