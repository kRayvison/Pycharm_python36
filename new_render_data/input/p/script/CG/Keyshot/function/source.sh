echo "to source hfs."
export _hfs_path=$1
echo _hfs_path=$_hfs_path
cd "${_hfs_path}"
source "${_hfs_path}/houdini_setup"
echo "source finished."