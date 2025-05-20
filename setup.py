from setuptools import setup, find_packages

setup(
    name='mkdocs-quiz-plugin',
    version='0.1.0',
    description='A MkDocs plugin to embed interactive quizzes in Markdown and JSON',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Sarah Weischer',
    author_email='you@example.com',
    url='https://github.com/yourusername/mkdocs-quiz-plugin',
    packages=find_packages(),
    install_requires=[
        'mkdocs>=1.0'
    ],
    entry_points={
        'mkdocs.plugins': [
            # register the plugin under the name 'quiz-plugin'
            'quiz-plugin = quiz_plugin.quiz_plugin:QuizPlugin'
        ]
    },
    classifiers=[
        'Framework :: MkDocs',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)