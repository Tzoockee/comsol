from distutils.core import setup
import py2exe
import sys
sys.path.append("..\\Shared\\")

MANIFEST_TEMPLATE = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="x86"
    name="%(prog)s"
    type="win32"
  />
  <description>Registratura Electronica by Comsol</description>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel
            level="asInvoker"
            uiAccess="false">
        </requestedExecutionLevel>
      </requestedPrivileges>
    </security>
  </trustInfo>
  <dependency>
    <dependentAssembly>
      <assemblyIdentity
            type="win32"
            name="Microsoft.VC90.CRT"
            version="9.0.21022.8"
            processorArchitecture="x86"
            publicKeyToken="1fc8b3b9a1e18e3b">
      </assemblyIdentity>
    </dependentAssembly>
  </dependency>
  <dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
  </dependency>
</assembly>
'''
RT_MANIFEST = 24

setup(
    name = 'Registratura Electronica by Comsol',
    version = '1.5',
    options = {
        'py2exe': {
            'dll_excludes': ['MSVCP90.dll'],
            'includes': 'decimal',
            'bundle_files': 1,
            'compressed': False,
            'optimize': 2,
            'dll_excludes': ['w9xpopen.exe', 'MSVCP90.dll']
        }
    },
    description = 'Registratura Electronica by Comsol',
    author = 'Comsol SRL',
    url = 'www.comsol.ro',
    zipfile = None,
    data_files=['client.cfg',
                  'comsol_logo.gif'],
    windows=[{
            'script':'client_ui.py',
            'other_resources' : [(RT_MANIFEST, 1, MANIFEST_TEMPLATE % dict(prog="client"))],
            }])