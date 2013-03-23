from setuptools import setup, find_packages

setup(
 name = 'opf_lib',
 version = "0.1",
 description = "OPF reading/writing library",
 packages = find_packages(),
 install_requires = ['html_stripper'],
 dependency_links = [
  'hg+http://hg.q-continuum.net/html_stripper#egg=html_stripper',
 ],
 classifiers = [
  'Development Status :: 5 - Stable',
  'Intended Audience :: Developers',
  'Programming Language :: Python',
  'License :: OSI Approved :: MIT License',
  'Topic :: Software Development :: Libraries',
 ],
)
