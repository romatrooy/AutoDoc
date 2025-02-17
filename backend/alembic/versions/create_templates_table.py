from alembic import op
import sqlalchemy as sa

revision = '002_create_templates_table'
down_revision = '001_create_users_table'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'templates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(), nullable=False),
        sa.Column('file_path', sa.String(), nullable=False),
        sa.Column('content_type', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_templates_filename'), 'templates', ['filename'], unique=False)
    op.create_index(op.f('ix_templates_id'), 'templates', ['id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_templates_id'), table_name='templates')
    op.drop_index(op.f('ix_templates_filename'), table_name='templates')
    op.drop_table('templates')
