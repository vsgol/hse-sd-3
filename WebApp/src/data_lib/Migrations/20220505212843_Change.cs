using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace data_lib.Migrations
{
    public partial class Change : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Comments_Attempts_AttemptId",
                table: "Comments");

            migrationBuilder.DropIndex(
                name: "IX_Comments_AttemptId",
                table: "Comments");

            migrationBuilder.AlterColumn<int>(
                name: "AttemptId",
                table: "Comments",
                type: "INTEGER",
                nullable: false,
                defaultValue: 0,
                oldClrType: typeof(int),
                oldType: "INTEGER",
                oldNullable: true);
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AlterColumn<int>(
                name: "AttemptId",
                table: "Comments",
                type: "INTEGER",
                nullable: true,
                oldClrType: typeof(int),
                oldType: "INTEGER");

            migrationBuilder.CreateIndex(
                name: "IX_Comments_AttemptId",
                table: "Comments",
                column: "AttemptId");

            migrationBuilder.AddForeignKey(
                name: "FK_Comments_Attempts_AttemptId",
                table: "Comments",
                column: "AttemptId",
                principalTable: "Attempts",
                principalColumn: "Id");
        }
    }
}
