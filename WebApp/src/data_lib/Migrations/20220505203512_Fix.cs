using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace data_lib.Migrations
{
    public partial class Fix : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Attempts_Tasks_TaskId",
                table: "Attempts");

            migrationBuilder.DropIndex(
                name: "IX_Attempts_TaskId",
                table: "Attempts");
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateIndex(
                name: "IX_Attempts_TaskId",
                table: "Attempts",
                column: "TaskId");

            migrationBuilder.AddForeignKey(
                name: "FK_Attempts_Tasks_TaskId",
                table: "Attempts",
                column: "TaskId",
                principalTable: "Tasks",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);
        }
    }
}
