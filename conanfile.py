from conans import ConanFile, tools
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
import os

class Conan(ConanFile):
    name = "zlib"
    version = "1.2.12"
    description = "A Massively Spiffy Yet Delicately Unobtrusive Compression Library " \
                  "(Also Free, Not to Mention Unencumbered by Patents)"
    homepage = "https://zlib.net/"
    license = "Zlib"
    url = f"https://github.com/ssrobins/conan-{name}"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "CMakeDeps"
    revision_mode = "scm"
    exports_sources = ["CMakeLists.diff", "CMakeLists.txt"]
    zip_folder_name = f"{name}-{version}"
    zip_name = f"{zip_folder_name}.tar.gz"
    build_subfolder = "build"
    source_subfolder = "source"

    def build_requirements(self):
        self.build_requires("cmake_utils/7.0.0#9bf47716aeee70a8dcfc8592831a0318eb327a09")

    def source(self):
        tools.get(f"https://zlib.net/{self.zip_name}",
            sha256="91844808532e5ce316b3c010929493c0244f3d37593afd6de04f71821d5136d9")
        os.rename(self.zip_folder_name, self.source_subfolder)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generator = "Ninja Multi-Config"
        tc.variables["CMAKE_VERBOSE_MAKEFILE"] = "TRUE"
        if self.settings.os == "iOS" and self.settings.arch != "x86_64":
            tc.blocks["apple_system"].values["cmake_osx_architectures"] = "armv7;arm64"
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        #with tools.chdir(self.build_subfolder):
        #     self.run(f"ctest -C {self.settings.build_type} --output-on-failure")

    def package(self):
        self.copy("*.h", dst="include", src=self.source_subfolder)
        self.copy("*.h", dst="include", src=self.build_folder, keep_path=False)
        self.copy("build/lib/zlibstatic*.lib", dst="lib", keep_path=False)
        self.copy("build/lib/*.a", dst="lib", keep_path=False)
        if self.settings.compiler == "msvc":
            self.copy("*.pdb", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows" and not tools.os_info.is_linux:
            if self.settings.build_type == "Debug":
                self.cpp_info.libs = ["zlibstaticd"]
            else:
                self.cpp_info.libs = ["zlibstatic"]
        else:
            if self.settings.build_type == "Debug":
                self.cpp_info.libs = ["zd"]
            else:
                self.cpp_info.libs = ["z"]
