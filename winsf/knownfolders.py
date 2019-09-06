''' Lookup Windows special or known folders using ctypes.
    From Eryk Sun, https://stackoverflow.com/a/33181421/14420
'''
import ctypes
from ctypes import wintypes

__all__ = ['FOLDERID', 'get_known_folder_path']

_ole32 = ctypes.OleDLL('ole32')
_shell32 = ctypes.OleDLL('shell32')

class GUID(ctypes.Structure):
    _fields_ = (('Data1', ctypes.c_ulong),
                ('Data2', ctypes.c_ushort),
                ('Data3', ctypes.c_ushort),
                ('Data4', ctypes.c_char * 8))
    def __init__(self, guid_string):
        _ole32.IIDFromString(guid_string, ctypes.byref(self))

REFKNOWNFOLDERID = LPIID = ctypes.POINTER(GUID)

_ole32.IIDFromString.argtypes = (
    wintypes.LPCWSTR, # lpsz,
    LPIID)            # lpiid

_ole32.CoTaskMemFree.restype = None
_ole32.CoTaskMemFree.argtypes = (wintypes.LPVOID,)

_shell32.SHGetKnownFolderPath.argtypes = (
    REFKNOWNFOLDERID, # rfid
    wintypes.DWORD,   # dwFlags
    wintypes.HANDLE,  # hToken
    ctypes.POINTER(wintypes.LPWSTR)) # ppszPath

def get_known_folder_path(folder_id, htoken=None):
    pszPath = wintypes.LPWSTR()
    _shell32.SHGetKnownFolderPath(ctypes.byref(folder_id),
                                  0, htoken, ctypes.byref(pszPath))
    folder_path = pszPath.value
    _ole32.CoTaskMemFree(pszPath)
    return folder_path

try:
    from win32com.shell import shell, shellcon
except ImportError:
    pass
else:
    __all__ += ['get_known_folder_id_list', 'list_known_folder']

    PPITEMIDLIST = ctypes.POINTER(ctypes.c_void_p)

    _shell32.SHGetKnownFolderIDList.argtypes = (
        REFKNOWNFOLDERID, # rfid
        wintypes.DWORD,   # dwFlags
        wintypes.HANDLE,  # hToken
        PPITEMIDLIST)     # ppidl

    def get_known_folder_id_list(folder_id, htoken=None):
        pidl = ctypes.c_void_p()
        _shell32.SHGetKnownFolderIDList(ctypes.byref(folder_id),
                                        0, htoken, ctypes.byref(pidl))
        folder_id_list = shell.AddressAsPIDL(pidl.value)
        _ole32.CoTaskMemFree(pidl)
        return folder_id_list

    def list_known_folder(folder_id, htoken=None):
        result = []
        pidl = get_known_folder_id_list(folder_id, htoken)
        shell_item = shell.SHCreateShellItem(None, None, pidl)
        shell_enum = shell_item.BindToHandler(None, shell.BHID_EnumItems,
            shell.IID_IEnumShellItems)
        for item in shell_enum:
            result.append(item.GetDisplayName(shellcon.SIGDN_NORMALDISPLAY))
        result.sort(key=lambda x: x.upper())
        return result

# KNOWNFOLDERID
# https://msdn.microsoft.com/en-us/library/dd378457

# fixed
FOLDERID_Windows         = GUID('{F38BF404-1D43-42F2-9305-67DE0B28FC23}')
FOLDERID_System          = GUID('{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}')
FOLDERID_SystemX86       = GUID('{D65231B0-B2F1-4857-A4CE-A8E7C6EA7D27}')
FOLDERID_Fonts           = GUID('{FD228CB7-AE11-4AE3-864C-16F3910AB8FE}')
FOLDERID_ResourceDir     = GUID('{8AD10C31-2ADB-4296-A8F7-E4701232C972}')
FOLDERID_UserProfiles    = GUID('{0762D272-C50A-4BB0-A382-697DCD729B80}')
FOLDERID_Profile         = GUID('{5E6C858F-0E22-4760-9AFE-EA3317B67173}')
FOLDERID_Public          = GUID('{DFDF76A2-C82A-4D63-906A-5644AC457385}')
FOLDERID_ProgramData     = GUID('{62AB5D82-FDC1-4DC3-A9DD-070D1D495D97}')
FOLDERID_ProgramFiles    = GUID('{905e63b6-c1bf-494e-b29c-65b732d3d21a}')
FOLDERID_ProgramFilesX64 = GUID('{6D809377-6AF0-444b-8957-A3773F02200E}')
FOLDERID_ProgramFilesX86 = GUID('{7C5A40EF-A0FB-4BFC-874A-C0F2E0B9FA8E}')
FOLDERID_ProgramFilesCommon    = GUID('{F7F1ED05-9F6D-47A2-AAAE-29D317C6F066}')
FOLDERID_ProgramFilesCommonX64 = GUID('{6365D5A7-0F0D-45E5-87F6-0DA56B6A4F7D}')
FOLDERID_ProgramFilesCommonX86 = GUID('{DE974D24-D9C6-4D3E-BF91-F4455120B917}')

# common
FOLDERID_PublicDesktop   = GUID('{C4AA340D-F20F-4863-AFEF-F87EF2E6BA25}')
FOLDERID_PublicDocuments = GUID('{ED4824AF-DCE4-45A8-81E2-FC7965083634}')
FOLDERID_PublicDownloads = GUID('{3D644C9B-1FB8-4f30-9B45-F670235F79C0}')
FOLDERID_PublicMusic     = GUID('{3214FAB5-9757-4298-BB61-92A9DEAA44FF}')
FOLDERID_PublicPictures  = GUID('{B6EBFB86-6907-413C-9AF7-4FC2ABF07CC5}')
FOLDERID_PublicVideos    = GUID('{2400183A-6185-49FB-A2D8-4A392A602BA3}')
FOLDERID_CommonStartMenu = GUID('{A4115719-D62E-491D-AA7C-E74B8BE3B067}')
FOLDERID_CommonPrograms  = GUID('{0139D44E-6AFE-49F2-8690-3DAFCAE6FFB8}')
FOLDERID_CommonStartup   = GUID('{82A5EA35-D9CD-47C5-9629-E15D2F714E6E}')
FOLDERID_CommonTemplates = GUID('{B94237E7-57AC-4347-9151-B08C6C32D1F7}')

# peruser
FOLDERID_Desktop          = GUID('{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}')
FOLDERID_Documents        = GUID('{FDD39AD0-238F-46AF-ADB4-6C85480369C7}')
FOLDERID_Downloads        = GUID('{374DE290-123F-4565-9164-39C4925E467B}')
FOLDERID_Music            = GUID('{4BD8D571-6D19-48D3-BE97-422220080E43}')
FOLDERID_Pictures         = GUID('{33E28130-4E1E-4676-835A-98395C3BC3BB}')
FOLDERID_Videos           = GUID('{18989B1D-99B5-455B-841C-AB7C74E4DDFC}')
FOLDERID_LocalAppData     = GUID('{F1B32785-6FBA-4FCF-9D55-7B8E7F157091}')
FOLDERID_LocalAppDataLow  = GUID('{A520A1A4-1780-4FF6-BD18-167343C5AF16}')
FOLDERID_RoamingAppData   = GUID('{3EB685DB-65F9-4CF6-A03A-E3EF65729F3D}')
FOLDERID_StartMenu        = GUID('{625B53C3-AB48-4EC1-BA1F-A1EF4146FC19}')
FOLDERID_Programs         = GUID('{A77F5D77-2E2B-44C3-A6A2-ABA601054A51}')
FOLDERID_Startup          = GUID('{B97D20BB-F46A-4C97-BA10-5E3608430854}')
FOLDERID_Templates        = GUID('{A63293E8-664E-48DB-A079-DF759E0509F7}')
FOLDERID_UserProgramFiles = GUID('{5CD7AEE2-2219-4A67-B85D-6C9CE15660CB}')

# virtual
FOLDERID_AppsFolder       = GUID('{1e87508d-89c2-42f0-8a7e-645a0f50ca58}')

# win32com defines most of these, except the ones added in Windows 8.
FOLDERID_AccountPictures  = GUID('{008ca0b1-55b4-4c56-b8a8-4de4b299d3be}')
FOLDERID_CameraRoll       = GUID('{AB5FB87B-7CE2-4F83-915D-550846C9537B}')
FOLDERID_PublicUserTiles  = GUID('{0482af6c-08f1-4c34-8c90-e17ec98b1e17}')
FOLDERID_RoamedTileImages = GUID('{AAA8D5A5-F1D6-4259-BAA8-78E7EF60835E}')
FOLDERID_RoamingTiles     = GUID('{00BCFC5A-ED94-4e48-96A1-3F6217F21990}')
FOLDERID_Screenshots      = GUID('{b7bede81-df94-4682-a7d8-57a52620b86f}')
FOLDERID_SearchHistory    = GUID('{0D4C3DB6-03A3-462F-A0E6-08924C41B5D4}')
FOLDERID_SearchTemplates  = GUID('{7E636BFE-DFA9-4D5E-B456-D7B39851D8A9}')
FOLDERID_ApplicationShortcuts = GUID('{A3918781-E5F2-4890-B3D9-A7E54332328C}')
FOLDERID_HomeGroupCurrentUser = GUID('{9B74B6A3-0DFD-4f11-9E78-5F7800F2E772}')
FOLDERID_SkyDrive             = GUID('{A52BBA46-E9E1-435f-B3D9-28DAA648C0F6}')
FOLDERID_SkyDriveCameraRoll   = GUID('{767E6811-49CB-4273-87C2-20F355E1085B}')
FOLDERID_SkyDriveDocuments    = GUID('{24D89E24-2F19-4534-9DDE-6A6671FBB8FE}')
FOLDERID_SkyDrivePictures     = GUID('{339719B5-8C47-4894-94C2-D8F77ADD44A6}')

class SimpleNamespace(object):
    def __init__(self, **kwds):
        vars(self).update(kwds)
    def __dir__(self):
        return [x for x in sorted(vars(self)) if not x.startswith('__')]

FOLDERID = SimpleNamespace(
    # fixed
    Windows = FOLDERID_Windows,
    System = FOLDERID_System,
    SystemX86 = FOLDERID_SystemX86,
    Fonts = FOLDERID_Fonts,
    ResourceDir = FOLDERID_ResourceDir,
    UserProfiles = FOLDERID_UserProfiles,
    Profile = FOLDERID_Profile,
    Public = FOLDERID_Public,
    ProgramData = FOLDERID_ProgramData,
    ProgramFiles = FOLDERID_ProgramFiles,
    ProgramFilesX64 = FOLDERID_ProgramFilesX64,
    ProgramFilesX86 = FOLDERID_ProgramFilesX86,
    ProgramFilesCommon = FOLDERID_ProgramFilesCommon,
    ProgramFilesCommonX64 = FOLDERID_ProgramFilesCommonX64,
    ProgramFilesCommonX86 = FOLDERID_ProgramFilesCommonX86,
    # common
    PublicDesktop=FOLDERID_PublicDesktop,
    PublicDocuments=FOLDERID_PublicDocuments,
    PublicDownloads=FOLDERID_PublicDownloads,
    PublicMusic=FOLDERID_PublicMusic,
    PublicPictures=FOLDERID_PublicPictures,
    PublicVideos=FOLDERID_PublicVideos,
    CommonStartMenu=FOLDERID_CommonStartMenu,
    CommonPrograms=FOLDERID_CommonPrograms,
    CommonStartup=FOLDERID_CommonStartup,
    CommonTemplates=FOLDERID_CommonTemplates,
    # user
    Desktop=FOLDERID_Desktop,
    Documents=FOLDERID_Documents,
    Downloads=FOLDERID_Downloads,
    Music=FOLDERID_Music,
    Pictures=FOLDERID_Pictures,
    Videos=FOLDERID_Videos,
    LocalAppData=FOLDERID_LocalAppData,
    LocalAppDataLow=FOLDERID_LocalAppDataLow,
    RoamingAppData=FOLDERID_RoamingAppData,
    StartMenu=FOLDERID_StartMenu,
    Programs=FOLDERID_Programs,
    Startup=FOLDERID_Startup,
    Templates=FOLDERID_Templates,
    UserProgramFiles=FOLDERID_UserProgramFiles,
    # virtual
    AppsFolder=FOLDERID_AppsFolder,
    AccountPictures=FOLDERID_AccountPictures,
    CameraRoll=FOLDERID_CameraRoll,
    PublicUserTiles=FOLDERID_PublicUserTiles,
    RoamedTileImages=FOLDERID_RoamedTileImages,
    RoamingTiles=FOLDERID_RoamingTiles,
    Screenshots=FOLDERID_Screenshots,
    SearchHistory=FOLDERID_SearchHistory,
    SearchTemplates=FOLDERID_SearchTemplates,
    ApplicationShortcuts=FOLDERID_ApplicationShortcuts,
    HomeGroupCurrentUser=FOLDERID_HomeGroupCurrentUser,
    SkyDrive=FOLDERID_SkyDrive,
    SkyDriveCameraRoll=FOLDERID_SkyDriveCameraRoll,
    SkyDriveDocuments=FOLDERID_SkyDriveDocuments,
    SkyDrivePictures=FOLDERID_SkyDrivePictures,
)

table = {}
for fid in dir(FOLDERID):
    try:
        path = get_known_folder_path(getattr(FOLDERID, fid))
        table[fid] = path
    except OSError:
        table[fid] = None

if __name__ == '__main__':
    for fid in dir(FOLDERID):
        try:
            path = get_known_folder_path(getattr(FOLDERID, fid))
            print("%s = %s" % (fid, path))
        except OSError:
            pass
