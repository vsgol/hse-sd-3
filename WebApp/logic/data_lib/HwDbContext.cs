using Microsoft.EntityFrameworkCore.Design;
using Microsoft.Extensions.Configuration;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;
using Microsoft.Extensions.Configuration;

namespace data_lib;

using logic.Models;
using Microsoft.EntityFrameworkCore;
public class HwDbContext: DbContext
{
    //public HwDbContext(DbContextOptions<HwDbContext> options) : base(options) {}
    public DbSet<HwTask> Tasks => Set<HwTask>();
    public DbSet<Attempt> Attempts => Set<Attempt>();
    public DbSet<Comment> Comments => Set<Comment>();
    public string DbPath { get; }

    public HwDbContext()
    {
        var folder = Environment.SpecialFolder.LocalApplicationData;
        var path = Environment.GetFolderPath(folder);
        Console.WriteLine(path);
        DbPath = Path.Join(path, "data.db");
    }
    
    public HwDbContext(DbContextOptionsBuilder options)
    {
        var folder = Environment.SpecialFolder.LocalApplicationData;
        var path = Environment.GetFolderPath(folder);
        Console.WriteLine(path);
        DbPath = Path.Join(path, "data.db");
        options.UseSqlite($"Data Source={DbPath}");
    }
    
    protected override void OnConfiguring(DbContextOptionsBuilder options)
        => options.UseSqlite($"Data Source={DbPath}");
}

// public class DesignTimeDbContextFactory : IDesignTimeDbContextFactory<HwDbContext>
// {
//     public HwDbContext CreateDbContext(string[] args)
//     {
//         var builder = new DbContextOptionsBuilder<HwDbContext>();
//         builder.UseSqlite();
//         return new HwDbContext(builder.Options);
//     }
// }