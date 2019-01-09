from distutils.core import setup

setup(
    name="mercurial-server",
    description="Centralized Mercurial repository manager",
    url="http://www.lshift.net/mercurial-server.html",
    version="1.3p1",
    package_dir = {'': 'src'},
    packages = ["mercurialserver"],
    requires = ["mercurial"],
    scripts = ['src/hg-ssh', 'src/refresh-auth'],
    data_files = [
        ('conf', [
            'src/conf/access.conf',
            'src/conf/hgadmin-hgrc'
        ]),
    ],
)
