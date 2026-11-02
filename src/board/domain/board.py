import uuid
from dataclasses import dataclass
from typing import Literal

"""
1. 게시판은 무한대로 생성 가능하다. 게시판 설정 하나가 게시판 하나가 된다.
2. 게시판은 비회원, 회원, 관리자 모두 사용 가능하다.
3. 비회원, 회원, 관리자의 역할에 따라서 이용 제한을 설정할 수 있다.
4. 권한은 다음과 같다.
    - 게시글 수정 가능 권한(edit_role, editable): 글 쓰기, 글 수정, 글 삭제 가능
    - 게시글 상세 보기 가능 권한(view_role, viewable): 글 상세 열람 가능
    - 게시글 목록 보기 가능 권한(list_role, listable): 글 목록 열람 가능
    - 댓글 목록 보기 가능 권한(comment_list_role, comment_listable): 댓글 목록 열람 가능하다
    - 댓글 수정 가능 권한(comment_edit_role, comment_editable): 댓글 쓰기, 댓글 수정, 댓글 삭제 권한
5. 비회원으로 글 또는 댓글 작성시에는 비밀번호(6자리 이상)를 등록해야 하며, 글 또는 댓글 수정, 삭제시에 작성시에 등록한 비밀번호를 검증해야 한다.
6. 게시글 목록에서 노출될 게시글 갯수는 설정 가능해야 하며 기본값은 20이다.
"""

RoleType = Literal['ALL', 'USER', 'ADMIN']

@dataclass
class Board:
    id: str
    writer: "Writer"
    authority: "Authority"
    password_hash: str | None = None


# 글, 댓글 권한
@dataclass
class Authority:
    edit_role: RoleType = 'ALL'
    view_role: RoleType = 'ALL'
    list_role: RoleType = 'ALL'
    comment_list_role: RoleType = 'ALL'
    comment_edit_role: RoleType = 'ALL'

# 작성자
@dataclass
class Writer:
    user_id: uuid.UUID | None
    name: str