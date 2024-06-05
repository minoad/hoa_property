# Function to recursively get the directory tree
function Get-Tree {
    param (
        [string]$Path,
        [int]$Indent = 0
    )
    
    $indentString = ' ' * $Indent
    
    # Get directories
    Get-ChildItem -Path $Path -Directory | Where-Object { $_.Name -ne '.venv' } | ForEach-Object {
        "$indentString├── $($_.Name)/"
        Get-Tree -Path $_.FullName -Indent ($Indent + 4)
    }

    # Get files
    Get-ChildItem -Path $Path -File | ForEach-Object {
        "$indentString├── $($_.Name)"
    }
}

# Get the current directory
$currentDirectory = Get-Location

# Output the tree
Write-Output "$($currentDirectory.Name)/"
Get-Tree -Path $currentDirectory.FullName -Indent 0
