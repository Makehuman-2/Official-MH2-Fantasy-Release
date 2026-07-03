"""
    License information: data/licenses/makehuman_license.txt
    Author: black-punkduck

    Functions:
    * openGLError

    Classes:
    * GLDebug
"""

import OpenGL
from OpenGL import GL as gl

def openGLError():
    while True:
        a = gl.glGetError()
        if a == gl.GL_NO_ERROR:
            return
        print (a)

class GLDebug:
    """
    class for output of openGL parameters
    :param in osindex: index to specify OS (0=Windows, 1=Linux, 2=MacOS)
    :param bool initialized": indicates if openGL is already ininitialized
    """
    def __init__(self, osindex, initialized=True):
        self.initialized = initialized
        self.oldvers = (osindex == 2)
        #
        # minimal version for apple is 2.1
        self.min_version = tuple([2, 1]) if self.oldvers else tuple([3, 3])

    def getOpenGL_LibVers(self):
        return OpenGL.__version__

    def minVersion(self):
        return str(self.min_version)

    def getVersion(self):
        """
        get the openGL version, old version works with string
        """
        if self.initialized:
            if self.oldvers:
                version_string = gl.glGetString(gl.GL_VERSION).decode("utf-8")
                # Version string format: "X.Y..." (e.g., "2.1 Metal - 90.5")
                parts = version_string.split()[0].split('.')
                try:
                    major = int(parts[0])
                    minor = int(parts[1]) if len(parts) > 1 else 0
                    return(major, minor)
                except (ValueError, IndexError):
                    return(0, 0)
            else:
                return(gl.glGetIntegerv(gl.GL_MAJOR_VERSION, '*'), gl.glGetIntegerv(gl.GL_MINOR_VERSION, '*'))
        else:
            return(0,0)

    def checkVersion(self):
        major, minor = self.getVersion()
        return( (major, minor) >=  self.min_version)

    def getExtensions(self):
        """
        get extensions by trying to get them either with glGetStringi (valid from openGL 3.0) or with glgetString
        """
        extensions = []
        if self.initialized:
            if self.oldvers:
                ext_string = gl.glGetString(gl.GL_EXTENSIONS).decode("utf-8")
                if ext_string:
                    extensions = ext_string.split()
            else:
                n=  gl.glGetIntegerv(gl.GL_NUM_EXTENSIONS, "*")
                for i in range(0, n):
                    extensions.append (gl.glGetStringi(gl.GL_EXTENSIONS, i).decode("utf-8"))
        return (extensions)

    def getShadingLanguages(self):
        """
        get shading languages by trying to get them either with glGetStringi (valid from openGL 3.0) or with glgetString
        """
        languages = []
        if self.initialized:
            if self.oldvers:
                version_string = gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION).decode("utf-8")
                if version_string:
                    languages.append(version_string)
            else:
                n = int.from_bytes(gl.glGetIntegerv(gl.GL_NUM_SHADING_LANGUAGE_VERSIONS, "*"), "big")
                for i in range(0, n):
                    languages.append(gl.glGetStringi(gl.GL_SHADING_LANGUAGE_VERSION, i).decode("utf-8"))
        return (languages)

    def getCard(self):
        return gl.glGetString(gl.GL_VERSION).decode("utf-8") if self.initialized else "not initialized"

    def getRenderer(self):
        return gl.glGetString(gl.GL_RENDERER).decode("utf-8") if self.initialized else "not initialized"

    def getInfo(self):
        info = {}
        info["min_version"] = self.minVersion()
        info["version"] = self.getVersion()
        info["card"] = self.getCard()
        info["renderer"] = self.getRenderer()
        info["languages"] = self.getShadingLanguages()
        info["extensions"] = self.getExtensions()
        return(info)

    def getTextInfo(self):
        text = "Minimum version demanded: " + str(self.min_version) + \
            "<br>Highest version available: " + str(self.getVersion()) + \
            "<br>Card Driver: " + self.getCard() + \
            "<br>Renderer: " + self.getRenderer() + \
            "<p>Shading languages:"

        lang = self.getShadingLanguages()
        for l in lang:
            text += "<br>" + l

        text += "<p>Extensions:"
        ext = self.getExtensions()
        for l in ext:
            text += "<br>" + l

        return (text)



