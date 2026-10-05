"""HCIS initial locked schema"""
from alembic import op
from hcis.domain.models import Base
revision="0001"
down_revision=None

def upgrade():
    bind=op.get_bind()
    Base.metadata.create_all(bind=bind)

def downgrade():
    bind=op.get_bind()
    Base.metadata.drop_all(bind=bind)
