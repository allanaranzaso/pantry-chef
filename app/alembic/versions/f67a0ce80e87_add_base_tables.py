"""Add base tables

Revision ID: f67a0ce80e87
Revises:
Create Date: 2024-10-21 21:27:06.713849

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f67a0ce80e87'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'ingredient',
        sa.Column(
            'uuid',
            sa.Uuid(),
            server_default=sa.text('gen_random_uuid()'),
            nullable=False
        ),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('uom', sa.String(), server_default='each', nullable=False),
        sa.Column(
            'status',
            sa.String(length=20),
            server_default='draft',
            nullable=False
        ),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  server_default=sa.text('CURRENT_TIMESTAMP'),
                  nullable=False),
        sa.Column('last_updated_at', sa.TIMESTAMP(timezone=True),
                  server_default=sa.text('CURRENT_TIMESTAMP'),
                  nullable=False),
        sa.Column('last_modify_by', sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint('uuid')
    )

    op.create_table(
        'instruction',
        sa.Column(
            'uuid',
            sa.Uuid(),
            server_default=sa.text('gen_random_uuid()'),
            nullable=False
        ),
        sa.Column('step_number', sa.String(length=2), server_default='1',
                  nullable=False),
        sa.Column('description', sa.Text(),
                  server_default='There is no description available.',
                  nullable=False),
        sa.Column('duration_ms', sa.Float(), nullable=False),
        sa.Column('status', sa.String(length=20), server_default='draft',
                  nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  server_default=sa.text('CURRENT_TIMESTAMP'),
                  nullable=False),
        sa.Column('last_updated_at', sa.TIMESTAMP(timezone=True),
                  server_default=sa.text('CURRENT_TIMESTAMP'),
                  nullable=False),
        sa.Column('last_modify_by', sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint('uuid')
    )

    op.create_table(
        'recipe',
        sa.Column(
            'uuid',
            sa.Uuid(),
            server_default=sa.text('gen_random_uuid()'),
            nullable=False
        ),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('cuisine_type', sa.String(), nullable=False),
        sa.Column('status', sa.String(length=10), server_default='draft',
                  nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  server_default=sa.text('CURRENT_TIMESTAMP'),
                  nullable=False),
        sa.Column('last_updated_at', sa.TIMESTAMP(timezone=True),
                  server_default=sa.text('CURRENT_TIMESTAMP'),
                  nullable=False),
        sa.Column('last_modify_by', sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint('uuid')
    )

    op.create_table('recipe_ingredient_association',
                    sa.Column('recipe_uuid', sa.UUID(), nullable=False),
                    sa.Column('ingredient_uuid', sa.UUID(), nullable=False),
                    sa.ForeignKeyConstraint(['ingredient_uuid'], ['ingredient.uuid'], ),
                    sa.ForeignKeyConstraint(['recipe_uuid'], ['recipe.uuid'], )
                    )
    op.create_index('index_recipe_ingredient_association',
                    'recipe_ingredient_association', ['recipe_uuid', 'ingredient_uuid'],
                    unique=True)
    op.create_table('recipe_instruction_association',
                    sa.Column('recipe_uuid', sa.UUID(), nullable=False),
                    sa.Column('instruction_uuid', sa.UUID(), nullable=False),
                    sa.ForeignKeyConstraint(['instruction_uuid'], ['instruction.uuid'], ),
                    sa.ForeignKeyConstraint(['recipe_uuid'], ['recipe.uuid'], )
                    )
    op.create_index('index_recipe_instruction_association',
                    'recipe_instruction_association', ['recipe_uuid', 'instruction_uuid'],
                    unique=True)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('index_recipe_ingredient_association',
                  table_name='recipe_ingredient_association')
    op.drop_table('recipe_ingredient_association')
    op.drop_index('index_recipe_instruction_association',
                  table_name='recipe_instruction_association')
    op.drop_table('recipe_instruction_association')
    op.drop_table('recipe')
    op.drop_table('instruction')
    op.drop_table('ingredient')
    # ### end Alembic commands ###
