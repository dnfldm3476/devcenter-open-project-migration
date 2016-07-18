# -*- coding: utf-8 -*-
#!/usr/bin/env python
from .github import Github
from .naver import Naver
from os.path import exists
from os import makedirs
import webbrowser
import click
import os
from .helper import set_encoding, check_validate_project_name
import sys

set_encoding()

@click.command()
@click.option('--encoding',default='utf-8',help='Encoding of files')
@click.option('--github_repo',prompt=True,help='Name of github repo used for migration')
@click.option('--naver_repo',prompt=True,help='Name of naver project to migrate')
@click.option('--github_id',prompt=True,help='Github username')
@click.password_option('--github_pw',help='Github password')
@click.option('--naver_id',prompt=True,help='NAVER username')
@click.password_option('--naver_pw',help='NAVER password')
@click.option('--vcs',prompt=True,help='Version control system of open project')
def cli(encoding,github_repo,naver_repo,github_id,github_pw,
        naver_id,naver_pw,vcs):
    # 올바른 프로젝트인지 검증
    invalid_project_msg = '{0} 프로젝트는 존재하지 않습니다'.format(naver_repo)
    assert check_validate_project_name(naver_repo) is True, invalid_project_msg

    # github login
    gh = Github(github_id,github_pw,github_repo)

    # Making github repository
    gh.create_repo()

    # 위키 페이지를 만들 수 있도록 자동으로 웹 브라우저를 열어줌
    wiki_create_page_url = 'https://github.com/{0}/{1}/wiki/_new'.format(github_id,github_repo)

    if webbrowser.open(wiki_create_page_url):
        click.echo('Save Page 버튼을 눌러주세요!')

    # naver_repo의 소스 코드 저장소를 github_repo 로 migration
    migration_status = gh.migration_repo(vcs,naver_id,naver_pw,naver_repo)
    naver = Naver(naver_id,naver_pw,naver_repo,gh)

    # naver_repo 에 있는 이슈 게시판 다운로드를 파싱하기
    naver.parsing()
    gh.upload_asset_by_git()

if __name__ == '__main__':
    cli()
